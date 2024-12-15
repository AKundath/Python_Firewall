#!/usr/bin/env python3
import subprocess
import sys
import os
import time
from typing import List, Dict, Union

class NetworkConfigManager:
    def __init__(self):
        # Check if script is run with root privileges
        if os.geteuid() != 0:
            print("This script must be run as root. Please use sudo.")
            sys.exit(1)
        
        # Common services and their default ports
        self.common_services = {
            'HTTP': 80,
            'HTTPS': 443,
            'SSH': 22,
            'FTP': 21,
            'SMTP': 25,
            'SMTP (TLS)': 587,
            'POP3': 110,
            'POP3 (SSL)': 995,
            'IMAP': 143,
            'IMAP (SSL)': 993,
            'DNS': 53,
            'MySQL': 3306,
            'PostgreSQL': 5432,
            'Redis': 6379,
            'MongoDB': 27017,
            'RDP': 3389
        }

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')

    def check_ufw_status(self) -> Dict[str, Union[bool, str]]:
        """Check UFW status and return details."""
        try:
            status = subprocess.check_output(['ufw', 'status', 'verbose']).decode()
            is_active = 'Status: active' in status
            return {
                'active': is_active,
                'status_details': status
            }
        except subprocess.CalledProcessError as e:
            return {
                'active': False,
                'status_details': f"Error: {str(e)}"
            }

    def enable_ufw(self) -> bool:
        """Enable UFW firewall."""
        try:
            subprocess.run(['ufw', '--force', 'enable'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def disable_ufw(self) -> bool:
        """Disable UFW firewall."""
        try:
            subprocess.run(['ufw', 'disable'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def add_rule(self, port: int, protocol: str = 'tcp', action: str = 'allow') -> bool:
        """Add a new firewall rule."""
        try:
            subprocess.run(['ufw', action, f'{port}/{protocol}'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def delete_rule(self, port: int, protocol: str = 'tcp', action: str = 'allow') -> bool:
        """Delete an existing firewall rule."""
        try:
            subprocess.run(['ufw', 'delete', action, f'{port}/{protocol}'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def get_network_stats(self) -> Dict[str, str]:
        """Get network interface statistics."""
        stats = {}
        
        try:
            # Get network interfaces
            interfaces = subprocess.check_output(['ip', 'link', 'show']).decode()
            stats['interfaces'] = interfaces

            # Get IP addresses
            ips = subprocess.check_output(['ip', 'addr', 'show']).decode()
            stats['ip_addresses'] = ips

            # Get routing table
            routes = subprocess.check_output(['ip', 'route']).decode()
            stats['routing'] = routes

            # Get active connections
            connections = subprocess.check_output(['ss', '-tuln']).decode()
            stats['connections'] = connections

            return stats
        except subprocess.CalledProcessError as e:
            print(f"Error getting network stats: {str(e)}")
            return {}

    def apply_common_configurations(self, config_type: str) -> bool:
        """Apply predefined common configurations."""
        try:
            if config_type == "web_server":
                self.add_rule(80, 'tcp')   # HTTP
                self.add_rule(443, 'tcp')  # HTTPS
                self.add_rule(22, 'tcp')   # SSH
            elif config_type == "mail_server":
                self.add_rule(25, 'tcp')   # SMTP
                self.add_rule(587, 'tcp')  # SMTP (TLS)
                self.add_rule(993, 'tcp')  # IMAP (SSL)
                self.add_rule(995, 'tcp')  # POP3 (SSL)
            elif config_type == "secure_workstation":
                self.add_rule(22, 'tcp')   # SSH
                subprocess.run(['ufw', 'default', 'deny', 'incoming'], check=True)
                subprocess.run(['ufw', 'default', 'allow', 'outgoing'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def display_menu(self):
        """Display the main menu."""
        self.clear_screen()
        print("=== Ubuntu Network Configuration Tool ===")
        print("\nMain Menu:")
        print("1. Show Firewall Status")
        print("2. Enable Firewall")
        print("3. Disable Firewall")
        print("4. Manage Ports")
        print("5. Apply Predefined Configurations")
        print("6. Show Network Statistics")
        print("7. Exit")
        return input("\nEnter your choice (1-7): ")

    def display_services_menu(self):
        """Display the services menu."""
        self.clear_screen()
        print("=== Common Services ===")
        print("\nAvailable services:")
        for i, (service, port) in enumerate(self.common_services.items(), 1):
            print(f"{i}. {service} (Port {port})")
        print(f"{len(self.common_services) + 1}. Custom port")
        print(f"{len(self.common_services) + 2}. Back to main menu")
        
        return input(f"\nEnter your choice (1-{len(self.common_services) + 2}): ")

    def display_config_menu(self):
        """Display the predefined configurations menu."""
        self.clear_screen()
        print("=== Predefined Configurations ===")
        print("\nAvailable configurations:")
        print("1. Web Server (HTTP, HTTPS, SSH)")
        print("2. Mail Server (SMTP, IMAP, POP3)")
        print("3. Secure Workstation")
        print("4. Back to main menu")
        
        return input("\nEnter your choice (1-4): ")

    def handle_port_management(self):
        """Handle port management menu."""
        while True:
            self.clear_screen()
            print("=== Port Management ===")
            print("\n1. Open port for service")
            print("2. Close port")
            print("3. Back to main menu")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == '1':
                service_choice = self.display_services_menu()
                
                try:
                    service_idx = int(service_choice) - 1
                    if service_idx == len(self.common_services):
                        # Custom port
                        port = int(input("Enter the port number: "))
                        protocol = input("Enter protocol (tcp/udp) [tcp]: ").lower() or 'tcp'
                    elif service_idx < len(self.common_services):
                        service = list(self.common_services.keys())[service_idx]
                        port = self.common_services[service]
                        protocol = 'tcp'
                    else:
                        continue

                    if self.add_rule(port, protocol):
                        print(f"\nSuccessfully opened port {port}/{protocol}")
                    else:
                        print(f"\nFailed to open port {port}/{protocol}")
                    
                except ValueError:
                    print("\nInvalid input. Please enter a number.")
                input("\nPress Enter to continue...")
                
            elif choice == '2':
                try:
                    port = int(input("Enter the port number to close: "))
                    protocol = input("Enter protocol (tcp/udp) [tcp]: ").lower() or 'tcp'
                    
                    if self.delete_rule(port, protocol):
                        print(f"\nSuccessfully closed port {port}/{protocol}")
                    else:
                        print(f"\nFailed to close port {port}/{protocol}")
                except ValueError:
                    print("\nInvalid input. Please enter a number.")
                input("\nPress Enter to continue...")
                
            elif choice == '3':
                break

    def run(self):
        """Run the main program loop."""
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                self.clear_screen()
                status = self.check_ufw_status()
                print("\nFirewall Status:")
                print(status['status_details'])
                input("\nPress Enter to continue...")
                
            elif choice == '2':
                if self.enable_ufw():
                    print("\nFirewall has been enabled successfully.")
                else:
                    print("\nFailed to enable firewall.")
                input("\nPress Enter to continue...")
                
            elif choice == '3':
                if self.disable_ufw():
                    print("\nFirewall has been disabled successfully.")
                else:
                    print("\nFailed to disable firewall.")
                input("\nPress Enter to continue...")
                
            elif choice == '4':
                self.handle_port_management()
                
            elif choice == '5':
                config_choice = self.display_config_menu()
                if config_choice == '1':
                    self.apply_common_configurations('web_server')
                    print("\nWeb server configuration applied.")
                elif config_choice == '2':
                    self.apply_common_configurations('mail_server')
                    print("\nMail server configuration applied.")
                elif config_choice == '3':
                    self.apply_common_configurations('secure_workstation')
                    print("\nSecure workstation configuration applied.")
                input("\nPress Enter to continue...")
                
            elif choice == '6':
                self.clear_screen()
                stats = self.get_network_stats()
                if stats:
                    print("\n=== Network Interfaces ===")
                    print(stats['interfaces'])
                    print("\n=== IP Addresses ===")
                    print(stats['ip_addresses'])
                    print("\n=== Routing Table ===")
                    print(stats['routing'])
                    print("\n=== Active Connections ===")
                    print(stats['connections'])
                input("\nPress Enter to continue...")
                
            elif choice == '7':
                print("\nExiting...")
                sys.exit(0)
            
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)

def main():
    manager = NetworkConfigManager()
    manager.run()

if __name__ == "__main__":
    main()