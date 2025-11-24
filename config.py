"""
Configuration module for Password Manager.
Loads environment variables and provides configuration settings.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration class for the password manager."""
    
    # Master password (should be set via environment variable)
    MASTER_PASSWORD: str = os.getenv('MASTER_PASSWORD', '')
    
    # Database configuration
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_USER: str = os.getenv('DB_USER', 'root')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    DB_NAME: str = os.getenv('DB_NAME', 'password_manager_db')
    DB_PORT: int = int(os.getenv('DB_PORT', '3306'))
    
    # Encryption key (should be set via environment variable)
    # Generate with: from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())
    ENCRYPTION_KEY: Optional[bytes] = None
    
    @classmethod
    def load_encryption_key(cls) -> bytes:
        """Load or generate encryption key."""
        key_str = os.getenv('ENCRYPTION_KEY')
        if key_str:
            cls.ENCRYPTION_KEY = key_str.encode()
        else:
            # Generate a new key if none exists (WARNING: This should be saved)
            from cryptography.fernet import Fernet
            cls.ENCRYPTION_KEY = Fernet.generate_key()
            print("WARNING: Generated new encryption key. Save this to your .env file:")
            print(f"ENCRYPTION_KEY={cls.ENCRYPTION_KEY.decode()}")
        return cls.ENCRYPTION_KEY
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.MASTER_PASSWORD:
            raise ValueError("MASTER_PASSWORD must be set in environment variables")
        if not cls.DB_PASSWORD:
            raise ValueError("DB_PASSWORD must be set in environment variables")
        return True


# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please set required environment variables in .env file")
