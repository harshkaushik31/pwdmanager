"""
Encryption module for Password Manager.
Provides secure password encryption using Fernet (AES-128 in CBC mode).
"""

from cryptography.fernet import Fernet, InvalidToken
from typing import Optional
import base64
import hashlib


class EncryptionManager:
    """Handles encryption and decryption of passwords."""
    
    def __init__(self, key: bytes):
        """
        Initialize encryption manager with a key.
        
        Args:
            key: Encryption key (must be valid Fernet key)
        """
        try:
            self.cipher = Fernet(key)
        except Exception as e:
            raise ValueError(f"Invalid encryption key: {e}")
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt a plaintext password.
        
        Args:
            plaintext: The password to encrypt
            
        Returns:
            Base64-encoded encrypted password
        """
        if not plaintext:
            raise ValueError("Cannot encrypt empty password")
        
        try:
            encrypted_bytes = self.cipher.encrypt(plaintext.encode('utf-8'))
            return encrypted_bytes.decode('utf-8')
        except Exception as e:
            raise EncryptionError(f"Encryption failed: {e}")
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt an encrypted password.
        
        Args:
            ciphertext: The encrypted password
            
        Returns:
            Decrypted plaintext password
        """
        if not ciphertext:
            raise ValueError("Cannot decrypt empty ciphertext")
        
        try:
            decrypted_bytes = self.cipher.decrypt(ciphertext.encode('utf-8'))
            return decrypted_bytes.decode('utf-8')
        except InvalidToken:
            raise EncryptionError("Decryption failed: Invalid token or key mismatch")
        except Exception as e:
            raise EncryptionError(f"Decryption failed: {e}")
    
    @staticmethod
    def generate_key() -> bytes:
        """
        Generate a new Fernet encryption key.
        
        Returns:
            A new Fernet key
        """
        return Fernet.generate_key()
    
    @staticmethod
    def hash_master_password(password: str) -> str:
        """
        Hash the master password for secure comparison.
        
        Args:
            password: The master password
            
        Returns:
            SHA-256 hash of the password
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()


class EncryptionError(Exception):
    """Custom exception for encryption-related errors."""
    pass
