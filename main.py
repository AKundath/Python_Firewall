#!/usr/bin/env python3
import os
import sys
from system_update import SystemUpdater
from snapshot_manager import SnapshotManager
from FirewallScript import NetworkConfigManager
from ip_manager import IPManager

class SystemManager:
    def __init__(self):
        # Check if script is run with root privileges
        if os.geteuid() != 0:
            print("This script must be run as root. Please use sudo.")
            sys.exit(1)
            
        self.updater = SystemUpdater()
        self.snapshot = SnapshotManager()
        self.firewall = NetworkConfigManager()
        self.ipmanager = IPManager()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')

    def display_menu(self):
        """Display the main menu."""
        self.clear_screen()
        print("=== Ubuntu System Management Tool ===")
        print("\nMain Menu:")
        print("1. System Updates")
        print("2. System Snapshots")
        print("3. Firewall Management")
        print("4. IP Address Management")
        print("5. Exit")
        return input("\nEnter your choice (1-5): ")

    def run(self):
        """Run the main program loop."""
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                self.updater.run()
                
            elif choice == '2':
                self.snapshot.run()
                
            elif choice == '3':
                self.firewall.run()
                
            elif choice == '4':
                self.ipmanager.run()
            
            elif choice == '5':
                print("\nExiting...")
                sys.exit(0)
                
            else:
                print("\nInvalid choice. Please try again.")
                input("\nPress Enter to continue...")

def main():
    manager = SystemManager()
    manager.run()

if __name__ == "__main__":
    main()