import yaml
from netmiko import ConnectHandler
from datetime import datetime
import os

# === Load device inventory ===
with open("devices.yaml", "r") as f:
    inventory = yaml.safe_load(f)

group = "switches"
devices = inventory.get(group, [])

# === Load config commands ===
with open("config_commands.txt", "r") as f:
    config_commands = [line.strip() for line in f if line.strip()]

# === Create log folder ===
os.makedirs("logs", exist_ok=True)

# === Send configs to each device ===
for device in devices:
    hostname = device["host"]
    log_file = f"logs/{hostname}_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    print(f"\nConnecting to {hostname}...")
    try:
        conn = ConnectHandler(**device)
        conn.enable()

        print(f"Sending configuration to {hostname}...")
        output = conn.send_config_set(config_commands)

        with open(log_file, "w") as f:
            f.write(f"Config applied to {hostname}\n{'='*50}\n{output}\n")

        conn.disconnect()

    except Exception as e:
        print(f"Failed on {hostname}: {e}")
