"""
Database module for Password Manager.
Handles all database operations with proper connection management and security.
"""

import mysql.connector
from mysql.connector import Error, pooling
from typing import List, Dict, Optional, Any
from contextlib import contextmanager
import logging

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self):
        """Initialize database manager with connection pool."""
        self.connection_pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool."""
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name="password_manager_pool",
                pool_size=5,
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                port=Config.DB_PORT,
                autocommit=False
            )
            logger.info("Database connection pool initialized successfully")
        except Error as e:
            logger.error(f"Error creating connection pool: {e}")
            raise DatabaseError(f"Failed to initialize database: {e}")
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Yields:
            A database connection from the pool
        """
        connection = None
        try:
            connection = self.connection_pool.get_connection()
            yield connection
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise DatabaseError(f"Connection failed: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    def initialize_database(self):
        """Create the database and table if they don't exist."""
        try:
            # First connect without specifying database
            temp_pool = pooling.MySQLConnectionPool(
                pool_name="temp_pool",
                pool_size=1,
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=Config.DB_PORT
            )
            
            with temp_pool.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create database
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
                cursor.execute(f"USE {Config.DB_NAME}")
                
                # Create table with proper schema
                create_table_query = """
                CREATE TABLE IF NOT EXISTS pwdmanager (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    app_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password TEXT NOT NULL,
                    username VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_app_name (app_name),
                    INDEX idx_email (email),
                    UNIQUE KEY unique_app_username (app_name, username)
                )
                """
                cursor.execute(create_table_query)
                conn.commit()
                
                logger.info("Database and table initialized successfully")
                cursor.close()
                
        except Error as e:
            logger.error(f"Error initializing database: {e}")
            raise DatabaseError(f"Failed to initialize database: {e}")
    
    def insert_password(self, app_name: str, email: str, encrypted_password: str, 
                       username: str = "") -> bool:
        """
        Insert a new password record.
        
        Args:
            app_name: Name of the application/site
            email: User's email
            encrypted_password: Encrypted password
            username: Username (optional)
            
        Returns:
            True if successful
        """
        query = """
            INSERT INTO pwdmanager (app_name, email, password, username)
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (app_name, email, encrypted_password, username))
                conn.commit()
                cursor.close()
                logger.info(f"Password inserted for {app_name}")
                return True
        except Error as e:
            logger.error(f"Error inserting password: {e}")
            raise DatabaseError(f"Failed to insert password: {e}")
    
    def find_by_email(self, email: str) -> List[Dict[str, Any]]:
        """
        Find all accounts associated with an email.
        
        Args:
            email: Email to search for
            
        Returns:
            List of dictionaries containing account information
        """
        query = """
            SELECT id, app_name, email, password, username, created_at, updated_at
            FROM pwdmanager
            WHERE email = %s
            ORDER BY app_name
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, (email,))
                results = cursor.fetchall()
                cursor.close()
                return results
        except Error as e:
            logger.error(f"Error finding by email: {e}")
            raise DatabaseError(f"Failed to find accounts: {e}")
    
    def find_by_app_name(self, app_name: str) -> List[Dict[str, Any]]:
        """
        Find all accounts for a specific app/site.
        
        Args:
            app_name: Application name to search for
            
        Returns:
            List of dictionaries containing account information
        """
        query = """
            SELECT id, app_name, email, password, username, created_at, updated_at
            FROM pwdmanager
            WHERE app_name = %s
            ORDER BY username
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, (app_name,))
                results = cursor.fetchall()
                cursor.close()
                return results
        except Error as e:
            logger.error(f"Error finding by app name: {e}")
            raise DatabaseError(f"Failed to find passwords: {e}")
    
    def update_password(self, app_name: str, username: str, new_encrypted_password: str) -> bool:
        """
        Update password for an existing account.
        
        Args:
            app_name: Application name
            username: Username
            new_encrypted_password: New encrypted password
            
        Returns:
            True if successful
        """
        query = """
            UPDATE pwdmanager
            SET password = %s
            WHERE app_name = %s AND username = %s
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (new_encrypted_password, app_name, username))
                rows_affected = cursor.rowcount
                conn.commit()
                cursor.close()
                
                if rows_affected == 0:
                    raise DatabaseError("No matching record found to update")
                
                logger.info(f"Password updated for {app_name}/{username}")
                return True
        except Error as e:
            logger.error(f"Error updating password: {e}")
            raise DatabaseError(f"Failed to update password: {e}")
    
    def delete_password(self, app_name: str, username: str) -> bool:
        """
        Delete a password record.
        
        Args:
            app_name: Application name
            username: Username
            
        Returns:
            True if successful
        """
        query = """
            DELETE FROM pwdmanager
            WHERE app_name = %s AND username = %s
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (app_name, username))
                rows_affected = cursor.rowcount
                conn.commit()
                cursor.close()
                
                if rows_affected == 0:
                    raise DatabaseError("No matching record found to delete")
                
                logger.info(f"Password deleted for {app_name}/{username}")
                return True
        except Error as e:
            logger.error(f"Error deleting password: {e}")
            raise DatabaseError(f"Failed to delete password: {e}")
    
    def close(self):
        """Close all connections in the pool."""
        if self.connection_pool:
            # Connection pools don't have a direct close method
            # Connections are closed when they're returned to the pool
            logger.info("Database manager shutting down")


class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass
