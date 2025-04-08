# 🛠️ Cisco RSTP Automation with Python

Automates Spanning Tree Protocol (STP) configuration across Cisco switches using Python, Excel, and Netmiko.

This script enables **Rapid PVST**, removes global priority overrides, and delegates **Primary** and **Secondary Root Bridge** roles based on VLANs — all mapped from an Excel sheet.

---

## Features

- Enables `spanning-tree mode rapid-pvst`
- Removes `spanning-tree vlan 1-4094 priority 24576`
- Assigns root bridge roles per VLAN:
  - `Primary`: priority 0
  - `Secondary`: priority 4096
- Reads all configuration intent from Excel
- Includes logging, retries, and credential handling

---

## Excel Format

The script expects a `.xlsx` file with the following columns:

| IP Address | VLANs     | Root |
|------------|-----------|------|
| 10.1.1.1   | 10,20,30  | 1    |
| 10.1.1.2   | 10,20,30  | 2    |
| 10.1.1.3   |           |      |

- **IP Address** – Cisco switch IP
- **VLANs** – Comma-separated list of VLANs to target
- **Root** – `1` for Primary, `2` for Secondary (leave blank otherwise)

---

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/rstp-automation.git
   cd rstp-automation
