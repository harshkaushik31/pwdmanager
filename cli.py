"""
Command-line interface for Password Manager.
Provides user interaction and menu system.
"""

import getpass
import sys
from typing import Optional
import logging

from config import Config
from password_manager import PasswordManager, ValidationError
from database import DatabaseError
from encryption import EncryptionError

logger = logging.getLogger(__name__)


class CLI:
    """Command-line interface for the password manager."""
    
    def __init__(self):
        """Initialize CLI."""
        self.manager: Optional[PasswordManager] = None
        self.authenticated = False
    
    def run(self):
        """Main entry point for the CLI."""
        try:
            # Authenticate user
            if not self.authenticate():
                print("Authentication failed. Exiting.")
                return
            
            # Initialize password manager
            self._initialize_manager()
            
            # Main menu loop
            self._menu_loop()
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"\nAn unexpected error occurred: {e}")
        finally:
            if self.manager:
                self.manager.close()
    
    def authenticate(self) -> bool:
        """
        Authenticate the user with master password.
        
        Returns:
            True if authentication successful
        """
        print("=" * 80)
        print(" " * 25 + "PASSWORD MANAGER")
        print("=" * 80)
        print()
        
        max_attempts = 3
        for attempt in range(max_attempts):
            master_pwd = getpass.getpass("Enter master password: ")
            
            if master_pwd == Config.MASTER_PASSWORD:
                print("\n✓ Authentication successful!\n")
                self.authenticated = True
                return True
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"✗ Incorrect password. {remaining} attempt(s) remaining.\n")
                else:
                    print("✗ Maximum attempts exceeded.")
        
        return False
    
    def _initialize_manager(self):
        """Initialize the password manager."""
        try:
            encryption_key = Config.load_encryption_key()
            self.manager = PasswordManager(encryption_key)
            self.manager.initialize()
        except Exception as e:
            logger.error(f"Failed to initialize manager: {e}")
            print(f"Failed to initialize password manager: {e}")
            sys.exit(1)
    
    def _menu_loop(self):
        """Main menu loop."""
        while True:
            choice = self._display_menu()
            
            if choice == '1':
                self._create_password()
            elif choice == '2':
                self._find_by_email()
            elif choice == '3':
                self._find_by_app()
            elif choice == '4':
                self._update_password()
            elif choice == '5':
                self._delete_password()
            elif choice.upper() == 'Q':
                print("\nThank you for using Password Manager. Goodbye!")
                break
            else:
                print("✗ Invalid choice. Please try again.\n")
    
    def _display_menu(self) -> str:
        """
        Display the main menu and get user choice.
        
        Returns:
            User's menu choice
        """
        print("-" * 80)
        print(" " * 30 + "MAIN MENU")
        print("-" * 80)
        print("1. Create new password")
        print("2. Find all accounts by email")
        print("3. Find password for app/site")
        print("4. Update existing password")
        print("5. Delete password")
        print("Q. Exit")
        print("-" * 80)
        return input("\nEnter your choice: ").strip()
    
    def _create_password(self):
        """Handle password creation."""
        print("\n" + "=" * 80)
        print(" CREATE NEW PASSWORD")
        print("=" * 80)
        
        try:
            app_name = input("App/Site name: ").strip()
            email = input("Email: ").strip()
            password = getpass.getpass("Password: ")
            username = input("Username (optional, press Enter to skip): ").strip()
            
            self.manager.create_password(app_name, email, password, username)
            print("\n✓ Password created successfully!\n")
            
        except (ValidationError, EncryptionError, DatabaseError) as e:
            print(f"\n✗ Error: {e}\n")
        except Exception as e:
            logger.error(f"Unexpected error in create_password: {e}")
            print(f"\n✗ Unexpected error: {e}\n")
    
    def _find_by_email(self):
        """Handle finding accounts by email."""
        print("\n" + "=" * 80)
        print(" FIND ACCOUNTS BY EMAIL")
        print("=" * 80)
        
        try:
            email = input("Email: ").strip()
            accounts = self.manager.find_accounts_by_email(email)
            
            if not accounts:
                print("\n✗ No accounts found for this email.\n")
                return
            
            print(f"\n✓ Found {len(accounts)} account(s):\n")
            self._display_accounts(accounts)
            
        except (ValidationError, DatabaseError) as e:
            print(f"\n✗ Error: {e}\n")
        except Exception as e:
            logger.error(f"Unexpected error in find_by_email: {e}")
            print(f"\n✗ Unexpected error: {e}\n")
    
    def _find_by_app(self):
        """Handle finding password by app name."""
        print("\n" + "=" * 80)
        print(" FIND PASSWORD BY APP/SITE")
        print("=" * 80)
        
        try:
            app_name = input("App/Site name: ").strip()
            accounts = self.manager.find_password_by_app(app_name)
            
            if not accounts:
                print("\n✗ No accounts found for this app/site.\n")
                return
            
            print(f"\n✓ Found {len(accounts)} account(s):\n")
            self._display_accounts(accounts)
            
        except (ValidationError, DatabaseError) as e:
            print(f"\n✗ Error: {e}\n")
        except Exception as e:
            logger.error(f"Unexpected error in find_by_app: {e}")
            print(f"\n✗ Unexpected error: {e}\n")
    
    def _update_password(self):
        """Handle password update."""
        print("\n" + "=" * 80)
        print(" UPDATE PASSWORD")
        print("=" * 80)
        
        try:
            app_name = input("App/Site name: ").strip()
            username = input("Username: ").strip()
            new_password = getpass.getpass("New password: ")
            
            self.manager.update_password(app_name, username, new_password)
            print("\n✓ Password updated successfully!\n")
            
        except (ValidationError, EncryptionError, DatabaseError) as e:
            print(f"\n✗ Error: {e}\n")
        except Exception as e:
            logger.error(f"Unexpected error in update_password: {e}")
            print(f"\n✗ Unexpected error: {e}\n")
    
    def _delete_password(self):
        """Handle password deletion."""
        print("\n" + "=" * 80)
        print(" DELETE PASSWORD")
        print("=" * 80)
        
        try:
            app_name = input("App/Site name: ").strip()
            username = input("Username: ").strip()
            
            # Confirm deletion
            confirm = input(f"\nAre you sure you want to delete the password for {app_name}/{username}? (yes/no): ")
            if confirm.lower() != 'yes':
                print("\n✗ Deletion cancelled.\n")
                return
            
            self.manager.delete_password(app_name, username)
            print("\n✓ Password deleted successfully!\n")
            
        except (ValidationError, DatabaseError) as e:
            print(f"\n✗ Error: {e}\n")
        except Exception as e:
            logger.error(f"Unexpected error in delete_password: {e}")
            print(f"\n✗ Unexpected error: {e}\n")
    
    def _display_accounts(self, accounts):
        """
        Display accounts in a formatted table.
        
        Args:
            accounts: List of account dictionaries
        """
        # Calculate column widths
        col_widths = {
            'app': max(len('App/Site'), max(len(str(a.get('app_name', ''))) for a in accounts)),
            'email': max(len('Email'), max(len(str(a.get('email', ''))) for a in accounts)),
            'username': max(len('Username'), max(len(str(a.get('username', ''))) for a in accounts)),
            'password': max(len('Password'), 20)  # Min width for passwords
        }
        
        # Print header
        print("-" * (sum(col_widths.values()) + 13))
        print(f"| {'App/Site':<{col_widths['app']}} | {'Email':<{col_widths['email']}} | "
              f"{'Username':<{col_widths['username']}} | {'Password':<{col_widths['password']}} |")
        print("-" * (sum(col_widths.values()) + 13))
        
        # Print rows
        for account in accounts:
            app = str(account.get('app_name', ''))
            email = str(account.get('email', ''))
            username = str(account.get('username', ''))
            password = str(account.get('password', ''))
            
            print(f"| {app:<{col_widths['app']}} | {email:<{col_widths['email']}} | "
                  f"{username:<{col_widths['username']}} | {password:<{col_widths['password']}} |")
        
        print("-" * (sum(col_widths.values()) + 13))
        print()


def main():
    """Main entry point."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
