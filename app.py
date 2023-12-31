from flask import Flask, render_template, request, redirect, url_for, session
from helpers import login_required, logout_required, apology
from cs50 import SQL
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message, Mail
from flask_session import Session
from datetime import datetime
from io import BytesIO
import os
from flask_bootstrap import Bootstrap
import matplotlib.pyplot as plt
from validate_email_address import validate_email
import logging


app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize the database
db = SQL("sqlite:///mindscape.db")

# Make sure API key is set
os.environ["API_KEY"] = "sk_fbakoshg73nmak7379sr"
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
    
    
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # or 587
app.config['MAIL_USE_SSL'] = True  # or False
app.config['MAIL_USE_TLS'] = False  # or True
app.config['MAIL_USERNAME'] = 'MyMindScape@gmail.com'  # your email
app.config['MAIL_PASSWORD'] = 'Copyright@Ian&Jason'  # your email password
app.config['MAIL_DEFAULT_SENDER'] = 'MyMindScape@gmail.com'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college_experience_tracker.db'

def get_time_of_day():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Good Morning"
    elif 12 <= current_hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

# Route for the home page
@app.route('/')
@login_required  # Helper decorator to ensure the user is logged in
def home():
    user_data = db.execute("SELECT name FROM User WHERE user_id = ?", session["user_id"])
    moment = db.execute("SELECT * FROM moments WHERE user_id = ?", session['user_id'])

    # Get the time of day greeting
    greeting = get_time_of_day()

    if user_data:
        if user_data == [{'name': ''}]:
            user_data = user_data[0]['name']
        else:
            user_data = ", " + user_data[0]['name']
    else:
        user_data = "Name Not Found"

    return render_template('index.html', greeting=greeting, name=user_data, moment=moment)

    

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    """Register user"""

    # Check if the incoming request method is POST
    if request.method == "POST":
        # Retrieve the values submitted in the form: username, password, and confirmation
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")

        # If username is missing, give an apology message
        if not username:
            return apology("Missing Username", 400)
        elif not password:
            return apology("Missing Password", 400)                
        elif not confirmation:
            return apology("Missing Password Confirmation", 400)
        elif password != confirmation:
            return apology("Passwords Do Not Match", 400)
        elif not email:
            return apology("Missing Email", 400)
        
        #check if email is valid
        if not validate_email(email):
            return apology("Invalid Email", 400)
        
        #password must be at least 8 characters long and contain at least one number and one letter and one special character
        if len(password) < 8:
            return apology("Password must be at least 8 characters long", 400) 
        elif not any(char.isdigit() for char in password):
            return apology("Password must contain at least one number", 400) 
        elif not any(char.isalpha() for char in password):
            return apology("Password must contain at least one letter", 400) 
        elif not any(not char.isalnum() for char in password):
            return apology("Password must contain at least one special character", 400) 


        # Check whether there are similar usernames in the database
        existing_user = db.execute("SELECT * FROM User WHERE username = ?", username)

        # If the username already exists, give an apology message
        if existing_user:
            return apology("Username already exists", 400)

        # Add user information to the users table after passing all checks
        db.execute("INSERT INTO User (name, username, password, email) VALUES (?, ?, ?, ?)",
                    name, username, generate_password_hash(password), email)
       
        return redirect(url_for("login"))
        
    else:
        # Render the registration template for GET requests
        return render_template("register.html")


# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
@logout_required  
def login():
    # Check if the user is already logged in
    if session.get('user_id'):
        # If the user is already logged in, redirect to the home page
        return redirect(url_for('home'))
        
        # If the request method is POST, process the form data

    if request.method == 'POST':
        # Process login form data 
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if username and password were provided
        if not username or not password:
            return apology("Please provide both username and password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM User WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
                rows[0]["password"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        if rows and "user_id" in rows[0]:
            session["user_id"] = rows[0]["user_id"]
        else:
            # Handle the case where 'rows' is empty or 'id' is not in 'rows[0]'
            print("No 'id' found in 'rows'")

        # Redirect user to home page
        return redirect(url_for('home'))
    else:
        return render_template("login.html")


# Route for logging out
@app.route('/logout')
@login_required  # Use the helper decorator to ensure the user is logged in
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the login page after logout
    return render_template("logout.html")


# Route for recording a moment
@app.route('/moment', methods=['GET', 'POST'])
@login_required  # Use the helper decorator to ensure the user is logged in
def moment():
    if request.method == 'POST':
        try:
            # Process the form data
            date_str = request.form['date']
            description = request.form['description']

            # Validate and convert the date string to a datetime object
            date = datetime.strptime(date_str, '%Y-%m-%d')

            # Create a new entry object using the form data
            db.execute("INSERT INTO moments (user_id, date, description) VALUES (:user_id, :date, :description)", user_id=session['user_id'], date=date, description=description)

            # Redirect to the home page after successful recording
        
            return redirect(url_for('home'))


        except Exception as e:
            # Handle validation errors or database issues
            print(f'Error recording moment: {str(e)}')
            return redirect(url_for('record_moment'))

    else:
        # Render the record moment page if it's a GET request
        return render_template('moment.html')


from flask import abort

@app.route('/mood', methods=['GET', 'POST'])
def record_mood():
    if request.method == 'POST':
        try:
            # Retrieve the mood and intensity values from the form submission
            selected_mood = request.form['mood']
            intensity = int(request.form['intensity'])
            date_str = request.form['date']

            # Validate and convert the date string to a datetime object
            date = datetime.strptime(date_str, '%Y-%m-%d')

            # Retrieve user id and add current mood to the existing database using SQL
            db.execute("INSERT INTO mood (user_id, mood, intensity, date) VALUES (:user_id, :mood, :intensity, :date)", user_id=session['user_id'], mood=selected_mood, intensity=intensity, date=date)

            # Redirect to the home page 
            return redirect(url_for('home'))

        except Exception as e:
            # Log the exception for debugging
            print(f"Error adding mood to the database: {e}")

            # Return a generic apology message with a 500 status code
            return apology("An error occurred while processing your request", 500)
    else:
        # Render the record mood page if it's a GET request
        return render_template('mood.html')

# Route for sending periodic summaries
@app.route('/send_periodic_summary', methods=['GET'])
@login_required
def send_periodic_summary():
         # Define function get_mood_data_for_period
     def get_mood_data_for_period(user_id, period):
        # Retrieve the user's mood data from the database
        mood_data = db.execute("SELECT * FROM mood WHERE user_id = ?", user_id)
        # Calculate the start and end dates for the period
        if period == 'week':
            start_date = datetime.now() - timedelta(days=7)
            end_date = datetime.now()
        elif period == 'month':
            start_date = datetime.now() - timedelta(days=30)
            end_date = datetime.now()
        else:
            start_date = datetime.now() - timedelta(days=365)
            end_date = datetime.now()

        # Extract the mood data for the period
        mood_data_for_period = [entry for entry in mood_data if start_date <= entry.date <= end_date]

        return mood_data_for_period

    # Define function format_mood_summary
     def format_mood_summary(mood_data):
        # Process the mood data to extract relevant information for the summary
        dates = [entry.date for entry in mood_data]
        daily_moods = [entry.intensity for entry in mood_data]

        # Calculate the average mood for the period
        average_mood = sum(daily_moods) / len(daily_moods)

        # Calculate the mood for the most recent day
        current_mood = daily_moods[-1]

        # Calculate the mood for the previous day
        previous_mood = daily_moods[-2]

        # Calculate the mood change between the previous day and the current day
        mood_change = current_mood - previous_mood

        # Create a function to send email, using Flask-Mail. Body should be formatted summary, and title should be weekly mood summary

    # Define function send_email
     def send_email(to, subject, template):
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
    # function to get mood data for the past week or month
     mood_data = get_mood_data_for_period(session['user_id'], 'week') 

     #function to format mood data for display
     formatted_summary = format_mood_summary(mood_data) 

    # Use function send_email to send an email using Flask-Mail
     send_email(session['user_email'], 'Weekly Mood Summary', formatted_summary)  
     return "Periodic summary sent successfully!"



@app.route('/analytics')
@login_required
def analytics():
    try:
        # Retrieve mood data from the database
        mood_data = db.execute("SELECT mood, intensity FROM mood WHERE user_id = ?", (session['user_id'],))
    except Exception as e:
        print(f"Error retrieving mood data: {e}")
        mood_data = []

    # Process mood data to calculate mood counts and average intensity
    mood_counts = {}
    total_intensity = 0
    total_moods = 0

    for entry in mood_data:
        mood = entry['mood']
        intensity = entry['intensity']

        # Update mood counts
        mood_counts[mood] = mood_counts.get(mood, 0) + 1

        # Update total intensity
        total_intensity += intensity
        total_moods += 1

    # Calculate average intensity
    average_intensity = total_intensity / total_moods if total_moods > 0 else 0

    # Retrieve user data for displaying the name
    user_data = db.execute("SELECT name FROM User WHERE user_id = ?", session["user_id"])
    name = user_data[0]['name'] if user_data and user_data[0]['name'] else "Name Not Found"

    # Pass the mood counts, average intensity, and user name to the template
    return render_template('analytics.html', mood_counts=mood_counts, average_intensity=average_intensity, name=name)

# Error handler for all exceptions
@app.errorhandler(Exception)
def handle_error(e):
    print(f"An error occurred: {str(e)}")
    return apology("An Error Occurred", 403)

# Catch errors
if __name__ == '__main__':
    print("Reached app.run")
    app.run()