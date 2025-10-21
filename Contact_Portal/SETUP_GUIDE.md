# Complete Setup Guide

This guide provides detailed instructions for setting up the Contact Portal application.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Python Setup](#python-setup)
3. [MongoDB Setup](#mongodb-setup)
4. [Email Configuration](#email-configuration)
5. [Application Configuration](#application-configuration)
6. [Running the Application](#running-the-application)
7. [Testing](#testing)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Disk Space**: 500MB free space
- **Internet**: Required for MongoDB Atlas and email features

### Software Dependencies
- Python 3.8+
- MongoDB 4.4+ (local) or MongoDB Atlas account
- Gmail account (for email features)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Python Setup

### 1. Check Python Installation

```bash
python --version
```

If Python is not installed, download from [python.org](https://www.python.org/downloads/)

### 2. Create Virtual Environment

```bash
# Navigate to project directory
cd c:\Users\DR TARQUEEN\Desktop\contact_portal

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
pip list
```

You should see:
- Flask==3.0.0
- Flask-PyMongo==2.3.0
- Flask-Login==0.6.3
- Flask-Mail==0.9.1
- pymongo==4.6.0
- And other dependencies

## MongoDB Setup

### Option 1: Local MongoDB Installation

#### Windows
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Run installer (choose "Complete" installation)
3. Install as Windows Service (recommended)
4. Verify installation:
   ```bash
   mongod --version
   ```

#### macOS
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Linux (Ubuntu/Debian)
```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### Test Local Connection
```bash
# Connect to MongoDB shell
mongosh

# Or using Python
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/'); print('Connected:', client.server_info()['version'])"
```

### Option 2: MongoDB Atlas (Cloud)

#### 1. Create Account
- Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Sign up for free account
- Verify email

#### 2. Create Cluster
- Click "Build a Database"
- Choose "FREE" tier (M0)
- Select cloud provider and region (closest to you)
- Name your cluster (e.g., "ContactPortal")
- Click "Create Cluster" (takes 3-5 minutes)

#### 3. Create Database User
- Go to "Database Access"
- Click "Add New Database User"
- Choose "Password" authentication
- Username: `contactportal`
- Password: Generate secure password (save it!)
- Database User Privileges: "Read and write to any database"
- Click "Add User"

#### 4. Configure Network Access
- Go to "Network Access"
- Click "Add IP Address"
- For testing: Click "Allow Access from Anywhere" (0.0.0.0/0)
- For production: Add specific IP addresses
- Click "Confirm"

#### 5. Get Connection String
- Go to "Database" → "Connect"
- Choose "Connect your application"
- Driver: Python, Version: 3.12 or later
- Copy connection string:
  ```
  mongodb+srv://contactportal:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
  ```
- Replace `<password>` with your database user password
- Add database name: `contact_portal`
  ```
  mongodb+srv://contactportal:yourpassword@cluster0.xxxxx.mongodb.net/contact_portal?retryWrites=true&w=majority
  ```

## Email Configuration

### Gmail Setup for Password Reset

#### 1. Enable 2-Factor Authentication
- Go to [Google Account](https://myaccount.google.com/)
- Click "Security"
- Find "2-Step Verification"
- Click "Get Started" and follow instructions

#### 2. Generate App Password
- In Google Account → Security
- Under "2-Step Verification", find "App passwords"
- Click "App passwords"
- Select app: "Mail"
- Select device: "Other" (enter "Contact Portal")
- Click "Generate"
- Copy the 16-digit password (format: xxxx xxxx xxxx xxxx)
- **Important**: Save this password, you won't see it again!

#### 3. Alternative Email Providers

##### Outlook/Hotmail
```
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

##### Yahoo Mail
```
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
```

## Application Configuration

### 1. Create .env File

```bash
# Copy example file
copy .env.example .env
```

### 2. Edit .env File

Open `.env` in text editor and configure:

```bash
# Generate a secure secret key
# Option 1: Use Python
python -c "import secrets; print(secrets.token_hex(32))"

# Option 2: Use online generator
# Visit: https://randomkeygen.com/
```

Update `.env`:

```
# Flask Configuration
SECRET_KEY=your-generated-secret-key-here

# MongoDB Configuration
# For local:
MONGO_URI=mongodb://localhost:27017/contact_portal

# For Atlas:
# MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/contact_portal?retryWrites=true&w=majority

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-digit-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 3. Verify Configuration

Create `test_config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("Configuration Check:")
print(f"SECRET_KEY: {'✓' if os.getenv('SECRET_KEY') else '✗'}")
print(f"MONGO_URI: {'✓' if os.getenv('MONGO_URI') else '✗'}")
print(f"MAIL_USERNAME: {'✓' if os.getenv('MAIL_USERNAME') else '✗'}")
print(f"MAIL_PASSWORD: {'✓' if os.getenv('MAIL_PASSWORD') else '✗'}")
```

Run:
```bash
python test_config.py
```

## Running the Application

### 1. Start the Application

```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Run the application
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### 2. Access the Application

Open web browser and navigate to:
- Local: `http://localhost:5000`
- Network: `http://your-ip-address:5000`

### 3. Stop the Application

Press `Ctrl+C` in the terminal

## Testing

### 1. Test User Registration

1. Navigate to `http://localhost:5000/register`
2. Fill in:
   - Username: `testuser`
   - Email: `your-email@gmail.com`
   - Password: `Test123!`
   - Confirm Password: `Test123!`
3. Click "Register"
4. Verify success message

### 2. Test Login

1. Navigate to `http://localhost:5000/login`
2. Enter credentials
3. Click "Login"
4. Verify redirect to dashboard

### 3. Test Contact Management

1. Add a contact:
   - Mobile: `+1234567890`
   - Email: `contact@example.com`
   - Address: `123 Main St, City`
   - Registration: `REG001`
2. Verify contact appears in table
3. Search for contact using registration number
4. Verify search results

### 4. Test Password Reset

1. Logout
2. Click "Forgot Password?"
3. Enter your email
4. Check email inbox
5. Click reset link
6. Set new password
7. Login with new password

### 5. Verify Database

```bash
# Connect to MongoDB
mongosh

# Switch to database
use contact_portal

# Check collections
show collections

# View users
db.users.find().pretty()

# View contacts
db.contacts.find().pretty()
```

## Troubleshooting

### Python Issues

**Problem**: `python` command not found
```bash
# Try python3
python3 --version

# Or add Python to PATH (Windows)
# System Properties → Environment Variables → Path → Add Python directory
```

### MongoDB Issues

**Problem**: Connection refused
```bash
# Check if MongoDB is running
# Windows:
sc query MongoDB

# macOS/Linux:
sudo systemctl status mongod

# Start MongoDB
# Windows: Start from Services
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod
```

**Problem**: Authentication failed (Atlas)
- Verify username and password in connection string
- Check database user exists in Atlas
- Verify IP whitelist includes your IP

### Email Issues

**Problem**: Email not sending
- Verify 2FA is enabled on Gmail
- Regenerate App Password
- Check MAIL_USERNAME and MAIL_PASSWORD in .env
- Test with simple script:

```python
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'

mail = Mail(app)

with app.app_context():
    msg = Message('Test', recipients=['your-email@gmail.com'])
    msg.body = 'Test email'
    mail.send(msg)
    print('Email sent!')
```

### Port Issues

**Problem**: Port 5000 already in use
```bash
# Windows: Find and kill process
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Or change port in app.py
app.run(debug=True, port=5001)
```

## Production Deployment

### Security Checklist
- [ ] Change SECRET_KEY to strong random value
- [ ] Use environment variables (never commit .env)
- [ ] Enable HTTPS
- [ ] Set DEBUG=False
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Configure firewall
- [ ] Regular backups of MongoDB
- [ ] Update dependencies regularly
- [ ] Implement rate limiting
- [ ] Add logging

### Recommended Production Setup
- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Process Manager**: Supervisor or systemd
- **Database**: MongoDB Atlas (managed)
- **Hosting**: AWS, DigitalOcean, Heroku, or similar

## Next Steps

1. Customize templates in `templates/` folder
2. Add more features (edit contacts, export data, etc.)
3. Implement user roles and permissions
4. Add contact categories or tags
5. Create API endpoints for mobile apps
6. Add data validation and sanitization
7. Implement logging and monitoring

## Support

For issues or questions:
1. Check this guide
2. Review [README.md](README.md)
3. Check [QUICK_START.md](QUICK_START.md)
4. Search for similar issues online
5. Create issue in project repository

**Setup complete! You're ready to use Contact Portal! 🎉**
