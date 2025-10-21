from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import os
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER','noreply@contactportal.com')

# Initialize extensions
mongo = PyMongo(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if mongo.db.users.find_one({'username': username}):
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if mongo.db.users.find_one({'email': email}):
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow()
        })
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = mongo.db.users.find_one({'username': username})
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        user_data = mongo.db.users.find_one({'email': email})
        
        if user_data:
            # Generate reset token
            token = serializer.dumps(email, salt='password-reset-salt')
            
            # Create reset URL
            reset_url = url_for('reset_password', token=token, _external=True)
            
            # Send email
            try:
                # Check if email is configured
                if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
                    # For testing: Show reset link directly (NOT FOR PRODUCTION!)
                    flash(f'Email not configured. Reset link: {reset_url}', 'success')
                    print(f"Password reset link for {email}: {reset_url}")
                else:
                    msg = Message('Password Reset Request',
                                recipients=[email])
                    msg.body = f'''To reset your password, visit the following link:
https://cbca6d0dd175.ngrok-free.app/reset-password/{token}

This link will expire in 1 hour.

If you did not make this request, please ignore this email.
'''
                    mail.send(msg)
                    flash('Password reset instructions have been sent to your email', 'success')
            except Exception as e:
                flash(f'Error sending email: {str(e)}. Check console for details.', 'error')
                print(f"Email error details: {e}")
                print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
                print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
                print(f"Reset link (for testing): {reset_url}")
        else:
            # Don't reveal if email exists or not
            flash('If that email exists, password reset instructions have been sent', 'success')
        
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The reset link is invalid or has expired', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('reset_password.html')
        
        # Update password
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'email': email},
            {'$set': {'password': hashed_password}}
        )
        
        flash('Your password has been reset successfully', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Get all contacts for current user
    contacts = list(mongo.db.contacts.find({'user_id': current_user.id}))
    return render_template('dashboard.html', contacts=contacts)

@app.route('/add-contact', methods=['POST'])
@login_required
def add_contact():
    mobile = request.form.get('mobile')
    email = request.form.get('email')
    address = request.form.get('address')
    registration_number = request.form.get('registration_number')
    
    # Validation
    if not all([mobile, email, address, registration_number]):
        flash('All fields are required', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if registration number already exists for this user
    existing = mongo.db.contacts.find_one({
        'user_id': current_user.id,
        'registration_number': registration_number
    })
    
    if existing:
        flash('A contact with this registration number already exists', 'error')
        return redirect(url_for('dashboard'))
    
    # Add contact
    mongo.db.contacts.insert_one({
        'user_id': current_user.id,
        'mobile': mobile,
        'email': email,
        'address': address,
        'registration_number': registration_number,
        'created_at': datetime.utcnow()
    })
    
    flash('Contact added successfully', 'success')
    return redirect(url_for('dashboard'))

@app.route('/search-contact', methods=['POST'])
@login_required
def search_contact():
    registration_number = request.json.get('registration_number')
    
    if not registration_number:
        return jsonify({'error': 'Registration number is required'}), 400
    
    contact = mongo.db.contacts.find_one({
        'user_id': current_user.id,
        'registration_number': registration_number
    })
    
    if contact:
        contact['_id'] = str(contact['_id'])
        contact['created_at'] = contact['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return jsonify(contact)
    else:
        return jsonify({'error': 'Contact not found'}), 404

@app.route('/delete-contact/<contact_id>', methods=['POST'])
@login_required
def delete_contact(contact_id):
    result = mongo.db.contacts.delete_one({
        '_id': ObjectId(contact_id),
        'user_id': current_user.id
    })
    
    if result.deleted_count > 0:
        flash('Contact deleted successfully', 'success')
    else:
        flash('Contact not found', 'error')
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
