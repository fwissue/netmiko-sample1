import yaml
from netmiko import ConnectHandler
from datetime import datetime
import os

# === Load YAML ===
with open("devices.yaml", "r") as file:
    inventory = yaml.safe_load(file)

group = "switches"  # Change or pass as argument
devices = inventory.get(group, [])

# === Load commands from file ===
with open("commands.txt", "r") as file:
    commands = [line.strip() for line in file if line.strip()]

# === Create logs folder ===
os.makedirs("logs", exist_ok=True)

# === Run on each device ===
for device in devices:
    hostname = device.get("host")
    log_filename = f"logs/{hostname}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    print(f"\nConnecting to {hostname}... Logging to {log_filename}")
    try:
        connection = ConnectHandler(**device)
        connection.enable()

        with open(log_filename, "w") as log_file:
            log_file.write(f"Log for {hostname}\n")
            log_file.write(f"{'='*50}\n")

            for cmd in commands:
                output = connection.send_command(cmd)
                log_file.write(f"\n> {cmd}\n{output}\n")

        connection.disconnect()
    except Exception as e:
        print(f"Failed to connect to {hostname}: {e}")
