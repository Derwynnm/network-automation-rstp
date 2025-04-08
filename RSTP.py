import pandas as pd
import logging
import time
from netmiko import NetmikoTimeoutException, NetmikoAuthenticationException, ConnectHandler
from credentials_example import username, password, secret  # Import credentials from a local file

# --- Setup logging ---
logging.basicConfig(filename='config_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# --- Load and clean Excel file ---
df = pd.read_excel(r'path/to/your/devices.xlsx')  # Adjust filename if needed
df = df.dropna(subset=['IP Address'])

# --- Loop through each valid row ---
for index, row in df.iterrows():
    ip = str(row['IP Address']).strip()
    root = str(row.get('Root', '')).strip()
    vlan_string = str(row.get('VLANs', '')).strip()
    print(f"\n Connecting to {ip}...")

    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
        'secret': secret if secret else None,
    }

    retries = 3
    connection = None

    for attempt in range(retries):
        try:
            connection = ConnectHandler(**device)
            if not connection.check_enable_mode():
                connection.enable()
            break
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            print(f" Attempt {attempt + 1} failed for {ip}: {e}")
            time.sleep(2)
    else:
        print(f" Could not connect to {ip} after {retries} attempts.")
        logging.error(f"Failed to connect to {ip} after {retries} attempts.")
        continue

     # --- Start building configuration commands ---
    commands = ['spanning-tree mode rapid-pvst']
    commands.append('no spanning-tree vlan 1-4094 priority 24576')

    
    # --- Normalize Root value ---
    root_value = row.get('Root', None)

    try:
        root = int(root_value)
    except (ValueError, TypeError):
        root = None

    # --- Root Bridge Logic ---
    if root in [1, 2] and isinstance(vlan_string, str):
        vlan_list = [v.strip() for v in vlan_string.split(',') if v.strip()]
        priority = '0' if root == 1 else '4096'
        print(f" Setting priority {priority} for VLANs {vlan_list} on {ip}")  # DEBUG LINE
        for vlan in vlan_list:
            commands.append(f'spanning-tree vlan {vlan} priority {priority}')

    commands.append('end')
    commands.append('wr')

    # --- Send config and log output ---
    try:
        output = connection.send_config_set(commands)
        print(f" Successfully configured {ip}:\n{output}")
        logging.info(f"Configured {ip} successfully.\n{output}")
    except Exception as e:
        print(f" Error sending config to {ip}: {e}")
        logging.error(f"Error sending config to {ip}: {e}")
    finally:
        connection.disconnect()

