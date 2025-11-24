"""
Password Manager core business logic.
Handles password operations with encryption and validation.
"""

import re
from typing import List, Dict, Optional, Any
import logging

from database import DatabaseManager, DatabaseError
from encryption import EncryptionManager, EncryptionError

logger = logging.getLogger(__name__)


class PasswordManager:
    """Core password manager with business logic."""
    
    def __init__(self, encryption_key: bytes):
        """
        Initialize password manager.
        
        Args:
            encryption_key: Encryption key for password encryption
        """
        self.db = DatabaseManager()
        self.encryptor = EncryptionManager(encryption_key)
    
    def initialize(self):
        """Initialize the database schema."""
        try:
            self.db.initialize_database()
            logger.info("Password manager initialized successfully")
        except DatabaseError as e:
            logger.error(f"Failed to initialize: {e}")
            raise
    
    def create_password(self, app_name: str, email: str, password: str, 
                       username: str = "") -> bool:
        """
        Create a new password entry.
        
        Args:
            app_name: Name of the application/site
            email: User's email
            password: Plain text password
            username: Username (optional)
            
        Returns:
            True if successful
            
        Raises:
            ValidationError: If input validation fails
            EncryptionError: If encryption fails
            DatabaseError: If database operation fails
        """
        # Validate inputs
        self._validate_app_name(app_name)
        self._validate_email(email)
        self._validate_password(password)
        
        try:
            # Encrypt password
            encrypted_password = self.encryptor.encrypt(password)
            
            # Store in database
            self.db.insert_password(app_name, email, encrypted_password, username)
            logger.info(f"Password created for {app_name}")
            return True
            
        except (EncryptionError, DatabaseError) as e:
            logger.error(f"Failed to create password: {e}")
            raise
    
    def find_accounts_by_email(self, email: str) -> List[Dict[str, Any]]:
        """
        Find all accounts associated with an email.
        
        Args:
            email: Email to search for
            
        Returns:
            List of account dictionaries with decrypted passwords
        """
        self._validate_email(email)
        
        try:
            accounts = self.db.find_by_email(email)
            
            # Decrypt passwords
            for account in accounts:
                try:
                    account['password'] = self.encryptor.decrypt(account['password'])
                except EncryptionError:
                    account['password'] = '[DECRYPTION FAILED]'
                    logger.warning(f"Failed to decrypt password for {account['app_name']}")
            
            return accounts
            
        except DatabaseError as e:
            logger.error(f"Failed to find accounts: {e}")
            raise
    
    def find_password_by_app(self, app_name: str) -> List[Dict[str, Any]]:
        """
        Find password(s) for a specific app/site.
        
        Args:
            app_name: Application name to search for
            
        Returns:
            List of account dictionaries with decrypted passwords
        """
        self._validate_app_name(app_name)
        
        try:
            accounts = self.db.find_by_app_name(app_name)
            
            # Decrypt passwords
            for account in accounts:
                try:
                    account['password'] = self.encryptor.decrypt(account['password'])
                except EncryptionError:
                    account['password'] = '[DECRYPTION FAILED]'
                    logger.warning(f"Failed to decrypt password for {account['app_name']}")
            
            return accounts
            
        except DatabaseError as e:
            logger.error(f"Failed to find passwords: {e}")
            raise
    
    def update_password(self, app_name: str, username: str, new_password: str) -> bool:
        """
        Update password for an existing account.
        
        Args:
            app_name: Application name
            username: Username
            new_password: New plain text password
            
        Returns:
            True if successful
        """
        self._validate_app_name(app_name)
        self._validate_password(new_password)
        
        try:
            # Encrypt new password
            encrypted_password = self.encryptor.encrypt(new_password)
            
            # Update in database
            self.db.update_password(app_name, username, encrypted_password)
            logger.info(f"Password updated for {app_name}/{username}")
            return True
            
        except (EncryptionError, DatabaseError) as e:
            logger.error(f"Failed to update password: {e}")
            raise
    
    def delete_password(self, app_name: str, username: str) -> bool:
        """
        Delete a password entry.
        
        Args:
            app_name: Application name
            username: Username
            
        Returns:
            True if successful
        """
        self._validate_app_name(app_name)
        
        try:
            self.db.delete_password(app_name, username)
            logger.info(f"Password deleted for {app_name}/{username}")
            return True
            
        except DatabaseError as e:
            logger.error(f"Failed to delete password: {e}")
            raise
    
    def close(self):
        """Close database connections."""
        self.db.close()
    
    @staticmethod
    def _validate_app_name(app_name: str):
        """Validate application name."""
        if not app_name or not app_name.strip():
            raise ValidationError("Application name cannot be empty")
        if len(app_name) > 255:
            raise ValidationError("Application name too long (max 255 characters)")
    
    @staticmethod
    def _validate_email(email: str):
        """Validate email format."""
        if not email or not email.strip():
            raise ValidationError("Email cannot be empty")
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError("Invalid email format")
    
    @staticmethod
    def _validate_password(password: str):
        """Validate password strength."""
        if not password:
            raise ValidationError("Password cannot be empty")
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long")
        if len(password) > 128:
            raise ValidationError("Password too long (max 128 characters)")


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass
