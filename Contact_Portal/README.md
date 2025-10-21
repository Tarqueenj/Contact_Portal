# Contact Portal - Flask + MongoDB Web Application

A complete web application for managing contacts with user authentication, password reset functionality, and contact search capabilities.

## Features

### 1. User Authentication
- **User Registration**: Create new accounts with username, email, and password
- **User Login**: Secure login with password hashing using Werkzeug
- **Forgot Password**: Email-based password reset with secure tokens (1-hour expiry)
- **Session Management**: Persistent login sessions using Flask-Login

### 2. Contact Management
- **Add Contacts**: Store contact information with 4 required fields:
  - Mobile phone number
  - Email address
  - Physical address
  - Registration number (unique identifier)
- **View All Contacts**: Display all contacts in a responsive table
- **Search Contacts**: Real-time AJAX search by registration number
- **Delete Contacts**: Remove contacts with confirmation

### 3. Security Features
- Password hashing with Werkzeug
- Secure session management
- CSRF protection
- Token-based password reset with expiration
- User-specific data isolation

## Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: MongoDB (local or Atlas)
- **Authentication**: Flask-Login
- **Email**: Flask-Mail (SMTP)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Icons**: Font Awesome 6.4.0

## Quick Start

### Prerequisites
- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas account)
- Gmail account with App Password (for email functionality)

### Installation

1. **Clone or download the project**
   ```bash
   cd c:\Users\DR TARQUEEN\Desktop\contact_portal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the following variables:
     ```
     SECRET_KEY=your-secret-key-here
     MONGO_URI=mongodb://localhost:27017/contact_portal
     MAIL_USERNAME=your-email@gmail.com
     MAIL_PASSWORD=your-gmail-app-password
     ```

5. **Start MongoDB**
   - For local MongoDB: Ensure MongoDB service is running
   - For MongoDB Atlas: Use your connection string in MONGO_URI

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open browser: `http://localhost:5000`

## Configuration Guide

### MongoDB Setup

#### Option 1: Local MongoDB
```
MONGO_URI=mongodb://localhost:27017/contact_portal
```

#### Option 2: MongoDB Atlas (Cloud)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Get connection string
4. Update MONGO_URI:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/contact_portal?retryWrites=true&w=majority
```

### Email Setup (Gmail)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Update .env file**:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-digit-app-password
   ```

## Usage Guide

### 1. Register a New Account
- Navigate to `/register`
- Fill in username, email, and password
- Click "Register"

### 2. Login
- Navigate to `/login`
- Enter username and password
- Click "Login"

### 3. Reset Password
- Click "Forgot Password?" on login page
- Enter your email address
- Check email for reset link
- Click link and set new password

### 4. Add Contact
- After login, fill in the contact form:
  - Mobile phone number
  - Email address
  - Address
  - Registration number
- Click "Add Contact"

### 5. Search Contact
- Enter registration number in search field
- Click "Search" or press Enter
- View contact details in results

### 6. Delete Contact
- Click "Delete" button next to contact
- Confirm deletion

## Project Structure

```
contact_portal/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── templates/             # HTML templates
    ├── base.html          # Base template with navigation
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── forgot_password.html   # Forgot password page
    ├── reset_password.html    # Reset password page
    └── dashboard.html     # Main dashboard with contacts
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Redirect to login or dashboard | No |
| GET/POST | `/register` | User registration | No |
| GET/POST | `/login` | User login | No |
| GET | `/logout` | User logout | Yes |
| GET/POST | `/forgot-password` | Request password reset | No |
| GET/POST | `/reset-password/<token>` | Reset password with token | No |
| GET | `/dashboard` | View all contacts | Yes |
| POST | `/add-contact` | Add new contact | Yes |
| POST | `/search-contact` | Search by registration number | Yes |
| POST | `/delete-contact/<id>` | Delete contact | Yes |

## Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "username": String,
  "email": String,
  "password": String (hashed),
  "created_at": DateTime
}
```

### Contacts Collection
```json
{
  "_id": ObjectId,
  "user_id": String,
  "mobile": String,
  "email": String,
  "address": String,
  "registration_number": String,
  "created_at": DateTime
}
```

## Troubleshooting

### MongoDB Connection Issues
- Verify MongoDB is running: `mongod --version`
- Check connection string in `.env`
- For Atlas: Whitelist your IP address

### Email Not Sending
- Verify Gmail App Password is correct
- Check 2FA is enabled on Gmail
- Verify SMTP settings in `.env`

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process using port 5000

## Security Notes

- Never commit `.env` file to version control
- Change `SECRET_KEY` in production
- Use strong passwords
- Enable HTTPS in production
- Regularly update dependencies

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please create an issue in the project repository.
