# Password Manager

A secure, command-line password manager built with Python and MySQL, featuring strong encryption and professional architecture.

## Features

- 🔐 **Strong Encryption**: Uses Fernet (AES-128 CBC) for secure password encryption
- 🛡️ **Secure Authentication**: Master password protection with secure input (no echo)
- 💾 **Database-Backed**: MySQL database with connection pooling for reliability
- ✅ **Input Validation**: Email, password strength, and data validation
- 🏗️ **Professional Architecture**: Modular design with separation of concerns
- 📝 **Comprehensive Logging**: Track operations and debug issues
- 🔒 **SQL Injection Protection**: Parameterized queries for security
- 🎯 **User-Friendly CLI**: Clean, intuitive command-line interface

## Security Features

- **No Hardcoded Secrets**: All sensitive data stored in environment variables
- **Strong Encryption**: Industry-standard Fernet encryption for passwords
- **Secure Password Input**: Uses `getpass` to hide password input
- **Prepared Statements**: Prevents SQL injection attacks
- **Unique Constraints**: Prevents duplicate entries
- **Authentication Limits**: Maximum 3 login attempts

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MayankDew08/pwdmanager.git
   cd pwdmanager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**
   - Install MySQL if not already installed
   - Start MySQL service
   - Note your MySQL root password

4. **Configure environment variables**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set your values:
   ```env
   MASTER_PASSWORD=your_secure_master_password_here
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_database_password_here
   DB_NAME=password_manager_db
   DB_PORT=3306
   ```
   
   **Generate an encryption key:**
   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```
   
   Add the generated key to `.env`:
   ```env
   ENCRYPTION_KEY=your_generated_encryption_key_here
   ```

5. **Initialize the database**
   
   The application will automatically create the database and table on first run.

## Usage

Run the password manager:
```bash
python cli.py
```

### Main Menu Options

1. **Create new password** - Store a new password for an app/site
2. **Find all accounts by email** - View all accounts associated with an email
3. **Find password for app/site** - Search for passwords by app/site name
4. **Update existing password** - Change the password for an existing account
5. **Delete password** - Remove a password entry
6. **Q. Exit** - Quit the application

### Example Workflow

```
1. Launch the application
2. Enter your master password
3. Choose option 1 to create a new password
4. Enter app name: "GitHub"
5. Enter email: "user@example.com"
6. Enter password: (your GitHub password)
7. Enter username: "username123"
8. Password stored securely!
```

## Architecture

### Project Structure

```
pwdmanager/
├── cli.py                  # Command-line interface
├── password_manager.py     # Core business logic
├── database.py            # Database operations
├── encryption.py          # Encryption/decryption
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Your config (DO NOT COMMIT)
└── README.md             # This file
```

### Modules

- **cli.py**: User interface and menu system
- **password_manager.py**: Business logic, validation, and password operations
- **database.py**: Database connection pooling and CRUD operations
- **encryption.py**: Fernet-based encryption/decryption
- **config.py**: Environment variable loading and validation

## Database Schema

```sql
CREATE TABLE pwdmanager (
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
);
```

## Security Considerations

⚠️ **Important Security Notes:**

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Keep your encryption key safe** - Lost keys mean lost passwords
3. **Use a strong master password** - This is your first line of defense
4. **Regular backups** - Back up your database regularly
5. **Secure your MySQL** - Use strong database passwords
6. **HTTPS only** - If accessing MySQL remotely, use encrypted connections

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/
```

### Code Quality

The codebase follows:
- PEP 8 style guidelines
- Type hints for better IDE support
- Comprehensive error handling
- Logging for debugging
- Modular, testable architecture

## Migration from Old Version

If you're upgrading from the old `pwdmanager.py`:

1. **Backup your data**:
   ```sql
   mysqldump -u root -p mydb1 pwdmanager > backup.sql
   ```

2. **Note**: The old version used a simple substitution cipher. Passwords will need to be re-encrypted with the new system for proper security.

3. **Re-add passwords**: Use the new CLI to create entries with proper encryption

## Troubleshooting

### "Configuration Error: MASTER_PASSWORD must be set"
- Ensure `.env` file exists and contains `MASTER_PASSWORD`

### "Failed to initialize database"
- Check MySQL is running: `mysql -u root -p`
- Verify database credentials in `.env`
- Ensure MySQL user has CREATE DATABASE permissions

### "Decryption failed: Invalid token"
- Encryption key may have changed
- Verify `ENCRYPTION_KEY` in `.env` matches the key used to encrypt data

### Connection Issues
- Check MySQL is running on the correct port
- Verify `DB_HOST` and `DB_PORT` in `.env`
- Test connection: `mysql -h localhost -u root -p`

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide
- Add type hints to new functions
- Include docstrings for classes and methods
- Add tests for new features
- Update README if adding new features

## License

This project is open source and available for educational purposes.

## Acknowledgments

- Built with [cryptography](https://cryptography.io/) for encryption
- Uses [python-dotenv](https://github.com/theskumar/python-dotenv) for configuration
- MySQL connector from [Oracle](https://dev.mysql.com/doc/connector-python/en/)

## Contact

For issues, questions, or suggestions, please open an issue on GitHub.

---

**⚠️ DISCLAIMER**: This password manager is provided as-is for educational purposes. While it implements security best practices, use at your own risk. Always maintain backups of your data.
