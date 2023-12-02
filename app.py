from flask import Flask, render_template, request, redirect, url_for, session
from helpers import login_required, logout_required
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)   # Set a random secret key for session management

# A list to store entries
entries = []


# Route for registration
@app.route('/register', methods=['GET', 'POST'])
@logout_required  # Use the helper decorator to ensure the user is not logged in
def register():
    if request.method == 'POST':
        # Process registration form data here

        # Add user to your data storage (e.g., database)
        
        # For now, we'll just redirect to the login page after successful registration
        return redirect(url_for('login'))

    # Render the registration page
    return render_template('registration.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
@logout_required  # Use the helper decorator to ensure the user is not logged in
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username and password match the dummy user
        if username == users['username'] and password == users['password']:
            # Store user information in the session
            session['user_id'] = users['user_id']
            session['username'] = users['username']

            # Redirect to the home page after successful login
            return redirect(url_for('home'))

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

# Route for the home page
@app.route('/')
@login_required  # Use the helper decorator to ensure the user is logged in
def home():
    # Render the home page with the retrieved entries
    return render_template('index.html', entries=entries)

# Route for recording a moment
@app.route('/record_moment', methods=['GET', 'POST'])
@login_required  # Use the helper decorator to ensure the user is logged in
def record_moment():
    if request.method == 'POST':
        # Retrieve form data from the submitted form
        date = request.form.get('date')
        description = request.form.get('description')
        mood = request.form.get('mood')

        # Create a new entry dictionary and add it to the list
        entry = {'date': date, 'description': description, 'mood': mood}
        entries.append(entry)

        # Redirect to the home page after submitting the form
        return redirect(url_for('home'))

    # Render the form to record a moment
    return render_template('moment_recording.html')

if __name__ == '__main__':
    app.run(debug=True)
