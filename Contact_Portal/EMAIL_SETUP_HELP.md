# Email Setup Help - Fix "Error sending email" Issue

## Problem
You're seeing "Error sending email. Please try again later." when clicking the forgot password button.

## Cause
The `.env` file is not configured with valid email credentials.

## Solution

### Quick Fix (For Testing Only)
I've updated the code to show the password reset link directly in the browser when email is not configured. This allows you to test the password reset functionality without setting up email.

**To use this:**
1. Restart your Flask application
2. Click "Forgot Password"
3. Enter a registered email address
4. The reset link will appear on the screen
5. Copy and paste the link in your browser to reset the password

### Permanent Fix (Setup Gmail)

#### Step 1: Edit .env File
Open `c:\Users\DR TARQUEEN\Desktop\contact_portal\.env` in a text editor.

#### Step 2: Get Gmail App Password

1. **Enable 2-Factor Authentication:**
   - Go to https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup process

2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" for app
   - Select "Other" for device (name it "Contact Portal")
   - Click "Generate"
   - Copy the 16-digit password (format: xxxx xxxx xxxx xxxx)
   - **Remove spaces** when pasting into .env

#### Step 3: Update .env File

```env
# Flask Configuration
SECRET_KEY=change-this-to-a-random-secret-key

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/contact_portal

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-actual-email@gmail.com
MAIL_PASSWORD=xxxxxxxxxxxxxxxx
MAIL_DEFAULT_SENDER=your-actual-email@gmail.com
```

**Replace:**
- `your-actual-email@gmail.com` with your Gmail address
- `xxxxxxxxxxxxxxxx` with your 16-digit App Password (no spaces!)

#### Step 4: Restart Flask Application

```bash
# Stop the current Flask app (Ctrl+C)
# Then restart:
python app.py
```

#### Step 5: Test

1. Go to http://localhost:5000/login
2. Click "Forgot Password?"
3. Enter your email address
4. Check your Gmail inbox for the reset email

## Alternative Email Providers

### Using Outlook/Hotmail
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=your-email@outlook.com
```

### Using Yahoo Mail
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@yahoo.com
```

## Troubleshooting

### Error: "Username and Password not accepted"
- Make sure you're using an **App Password**, not your regular Gmail password
- Verify 2-Factor Authentication is enabled
- Remove any spaces from the App Password

### Error: "Connection refused"
- Check your internet connection
- Verify MAIL_SERVER and MAIL_PORT are correct
- Check if your firewall is blocking port 587

### Error: "Sender address rejected"
- Make sure MAIL_USERNAME and MAIL_DEFAULT_SENDER are the same
- Verify the email address is correct

### Still Not Working?
Run this test script to diagnose the issue:

```python
# test_email.py
import os
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Change this
app.config['MAIL_PASSWORD'] = 'your-app-password'     # Change this

mail = Mail(app)

with app.app_context():
    try:
        msg = Message('Test Email',
                     sender='your-email@gmail.com',
                     recipients=['your-email@gmail.com'])
        msg.body = 'This is a test email from Contact Portal'
        mail.send(msg)
        print('✓ Email sent successfully!')
    except Exception as e:
        print(f'✗ Error: {e}')
```

Run: `python test_email.py`

## Current Workaround

Since I've updated the code, you can now test the password reset feature without email:

1. The reset link will be displayed on the screen
2. The link will also be printed in the console/terminal
3. Copy the link and paste it in your browser
4. Set your new password

**Note:** This workaround is for testing only. For production, you must configure proper email settings.

## Need More Help?

Check these resources:
- [Gmail App Passwords Guide](https://support.google.com/accounts/answer/185833)
- [Flask-Mail Documentation](https://pythonhosted.org/Flask-Mail/)
- README.md in this project
- SETUP_GUIDE.md for detailed instructions
