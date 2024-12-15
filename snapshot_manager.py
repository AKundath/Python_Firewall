#!/usr/bin/env python3
import subprocess
import os
import sys
from datetime import datetime

class SnapshotManager:
    def __init__(self):
        if os.geteuid() != 0:
            print("This script must be run as root. Please use sudo.")
            sys.exit(1)

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')

    def run_command(self, command, show_output=True):
        """Run a command and optionally show its output."""
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output and show_output:
                    print(output.strip())
            
            return process.returncode == 0
        except subprocess.CalledProcessError:
            return False

    def create_snapshot(self, description=None):
        """Create a Timeshift snapshot."""
        try:
            # Check if Timeshift is installed
            if not os.path.exists('/usr/bin/timeshift'):
                print("\nTimeshift is not installed. Installing now...")
                if not self.run_command(['apt', 'install', 'timeshift', '-y']):
                    print("Failed to install Timeshift")
                    return False

            # Create snapshot
            if description is None:
                description = f"Auto-snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            print("\nCreating system snapshot...")
            return self.run_command(['timeshift', '--create', '--comment', description])
        except Exception as e:
            print(f"Error creating snapshot: {str(e)}")
            return False

    def list_snapshots(self):
        """List existing snapshots."""
        try:
            print("\nExisting snapshots:")
            return self.run_command(['timeshift', '--list'])
        except Exception as e:
            print(f"Error listing snapshots: {str(e)}")
            return False

    def display_menu(self):
        """Display the snapshot menu."""
        self.clear_screen()
        print("=== System Snapshot Menu ===")
        print("\n1. Create snapshot with default name")
        print("2. Create snapshot with custom description")
        print("3. List existing snapshots")
        print("4. Back to main menu")
        return input("\nEnter your choice (1-4): ")

    def run(self):
        """Run the snapshot menu loop."""
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                if self.create_snapshot():
                    print("\nSnapshot created successfully")
                else:
                    print("\nFailed to create snapshot")
                input("\nPress Enter to continue...")
                
            elif choice == '2':
                description = input("\nEnter snapshot description: ")
                if self.create_snapshot(description):
                    print("\nSnapshot created successfully")
                else:
                    print("\nFailed to create snapshot")
                input("\nPress Enter to continue...")
                
            elif choice == '3':
                self.list_snapshots()
                input("\nPress Enter to continue...")
                
            elif choice == '4':
                break
            
            else:
                print("\nInvalid choice. Please try again.")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    snapshot = SnapshotManager()
    snapshot.run()