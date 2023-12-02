from flask import Flask, render_template, request, redirect, url_for, session
from helpers import login_required, logout_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import bcrypt
import re


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college_experience_tracker.db'
#initialize the database
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

# Define the mood model
class mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    daily_mood = db.Column(db.Integer, nullable=False)
#create a function to return a string when we add something
    def __repr__(self):
        return '<username %r>' % self.user_id

# Route for the home page
@app.route('/')
@login_required  # Use the helper decorator to ensure the user is logged in
def home():
    # Retrieve the entries for the logged-in user
    entries = mood.query.filter_by(user_id=session['user_id']).all()

    # Render the home page with the retrieved entries
    return render_template('index.html', entries=entries)

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
@logout_required  # Use the helper decorator to ensure the user is not logged in
def register():
    if request.method == 'POST':
        # Process registration form data here
        username = request.form['username']

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            # If the username already exists, redirect to the apology message, username already exists page
            return render_template('apology.html', message='Username already exists')

        password = request.form['password']
        name = request.form['name']
        date_of_birth = request.form['date_of_birth']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Check if the password meets the requirements
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            # If the password does not meet the requirements, redirect to the apology message, invalid password page
            return render_template('apology.html', message='Invalid password')

        # Create a new user object using the form data
        new_user = User(username=username, password=hashed_password, name=name, date_of_birth=date_of_birth)

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Flash a success message and redirect to the login page
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    # Render the registration page if it's a GET request or registration fails
    return render_template('register.html')
# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
@logout_required  # Use the helper decorator to ensure the user is not logged in
def login():
    #Check if the user is already logged in
    if session.get('user_id'):
        # If the user is already logged in, redirect to the home page
        return redirect(url_for('home'))
        # If the request method is POST, process the form data
    if request.method == 'POST':
        # Process login form data here
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user object from the database
        user = User.query.filter_by(username=username).first()

        #hash the password and check
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):

        # Check if the user exists and the password is correct
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            # If the user exists and the password is correct, log the user in
            session['user_id'] = user.user_id
            # Redirect to the home page after successful login
            return redirect(url_for('home'))
        else:
            # If the user does not exist or the password is incorrect, redirect to the apology message, invalid credentials page
            return render_template('apology.html', message='Invalid credentials')
     # Render the login page if it's a GET request or login fails
    return render_template('login.html')

# Route for logging out
@app.route('/logout')
@login_required  # Use the helper decorator to ensure the user is logged in
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the login page after logout
    return redirect(url_for('login'))



# Route for recording a moment
@app.route('/record_moment', methods=['GET', 'POST'])
@login_required  # Use the helper decorator to ensure the user is logged in
def record_moment():
   # get input from the form and record it in the mood table in the database
    if request.method == 'POST':
        # Process the form data here
        date = request.form['date']
        description = request.form['description']
        daily_mood = request.form['daily_mood']
        # Create a new entry object using the form data
        new_entry = mood(user_id=session['user_id'], date=date, description=description, daily_mood=daily_mood)
        # Add the new entry to the database
        db.session.add(new_entry)
        db.session.commit()
        # Redirect to the home page after successful login
        return redirect(url_for('home'))
    # Render the record moment page if it's a GET request
    return render_template('record_moment.html')


if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

