# Quick Start Guide - 5 Minutes Setup

Get your Contact Portal running in 5 minutes!

## Step 1: Install Python Dependencies (1 min)

```bash
cd c:\Users\DR TARQUEEN\Desktop\contact_portal
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Setup MongoDB (1 min)

### Option A: Local MongoDB
- Install MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community)
- Start MongoDB service
- Use default connection: `mongodb://localhost:27017/contact_portal`

### Option B: MongoDB Atlas (Cloud - Recommended)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create free account and cluster
3. Get connection string
4. Whitelist your IP (0.0.0.0/0 for testing)

## Step 3: Configure Environment (1 min)

Create `.env` file:

```bash
# Copy example file
copy .env.example .env
```

Edit `.env` with your settings:

```
SECRET_KEY=my-super-secret-key-12345
MONGO_URI=mongodb://localhost:27017/contact_portal
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
```

## Step 4: Setup Gmail App Password (1 min)

1. Go to [Google Account](https://myaccount.google.com/)
2. Security → 2-Step Verification → App passwords
3. Generate password for "Mail"
4. Copy 16-digit password to `.env` file

## Step 5: Run Application (1 min)

```bash
python app.py
```

Open browser: **http://localhost:5000**

## First Use

1. **Register**: Create your account at `/register`
2. **Login**: Use your credentials
3. **Add Contact**: Fill in the form with contact details
4. **Search**: Use registration number to find contacts

## Test Email Feature

1. Click "Forgot Password?" on login page
2. Enter your email
3. Check inbox for reset link
4. Click link and set new password

## Common Issues

### MongoDB Connection Failed
```bash
# Check MongoDB is running
mongod --version

# Or use MongoDB Atlas connection string
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/contact_portal
```

### Email Not Sending
- Verify Gmail App Password (not regular password)
- Enable 2FA on Gmail account
- Check MAIL_USERNAME and MAIL_PASSWORD in .env

### Port 5000 Already in Use
```python
# Edit app.py, change last line to:
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Customize templates in `templates/` folder
- Add more features to `app.py`

## Quick Commands Reference

```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Deactivate virtual environment
deactivate
```

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] MongoDB running (local or Atlas)
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] Gmail App Password set
- [ ] Application running on port 5000
- [ ] Can register and login
- [ ] Can add and search contacts
- [ ] Password reset email working

**You're all set! Happy coding! 🚀**
