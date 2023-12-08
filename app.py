from flask import Flask, render_template, request, redirect, url_for, session, flash
from helpers import login_required, logout_required, apology
from cs50 import SQL
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message, Mail
from flask_session import Session
from datetime import datetime
from io import BytesIO
import os
import matplotlib.pyplot as plt
from validate_email_address import validate_email

import base64

app = Flask(__name__)
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


# Route for the home page
@app.route('/')
@login_required  # Use the helper decorator to ensure the user is logged in
def home():
   return render_template('index.html')


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

        # If username is missing, flash an apology message
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

        # If the username already exists, flash an apology message
        if existing_user:
            return apology("Username already exists", 400)

        # Add user information to the users table after passing all checks
        db.execute("INSERT INTO User (name, username, password, email) VALUES (?, ?, ?, ?)",
                    name, username, generate_password_hash(password), email)
        db.execute("COMMIT")
        return redirect(url_for("login"))
        
    else:
        # Render the registration template for GET requests
        return render_template("register.html")


# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
@logout_required  # Use the helper decorator to ensure the user is not logged in
def login():
    # Check if the user is already logged in
    if session.get('user_id'):
        # If the user is already logged in, redirect to the home page
        return redirect(url_for('home'))
        # If the request method is POST, process the form data

    if request.method == 'POST':
        # Process login form data here
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
    return redirect(url_for('logout'))


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
            new_entry = mood(user_id=session['user_id'], date=date, description=description)

            # Add the new entry to the database
            db.session.add(new_entry)
            db.session.commit()

            # Flash a success message
            flash('Moment recorded successfully!', 'success')

            # Redirect to the home page after successful recording
            return redirect(url_for('home'))

        except Exception as e:
            # Handle validation errors or database issues
            flash(f'Error recording moment: {str(e)}', 'danger')
            return redirect(url_for('record_moment'))

    else:
        # Render the record moment page if it's a GET request
        return render_template('moment.html')


# Define the route to  mood
@app.route('/mood', methods=['POST'])
@login_required  # Ensure the user is logged in
def mood():
    if request.method == 'POST':
        try:
            # Retrieve the mood and intensity values from the form submission
            selected_mood = request.form['mood']
            intensity = int(request.form['intensity'])

            # Retrieve user id and add current mood to the existing database using SQL
            db.execute("INSERT INTO mood (user_id, mood, intensity) VALUES (?, ?, ?)",
                    (session['user_id'], selected_mood, intensity))

            # Commit changes to the database
            db.commit()

            # Redirect to the home page 
            return redirect(url_for('home'))

        except Exception as e:
            # Handle the exception
            print(f"Error adding mood to the database: {e}")
            return apology("Error adding mood to the database", 403)
    else:
        # Render the record moment page if it's a GET request
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
    # Assuming you have a function to get mood data for the past week or month
     mood_data = get_mood_data_for_period(session['user_id'], 'week')  # You need to implement this function

    # Assuming you have a function to format mood data for display
     formatted_summary = format_mood_summary(mood_data)  # You need to implement this function

    # Assuming you have a function to send an email using Flask-Mail
     send_email(session['user_email'], 'Weekly Mood Summary', formatted_summary)  # You need to implement this function

     return "Periodic summary sent successfully!"


@app.route('/analytics')
@login_required
def analytics():
    try:
        mood_data = db.execute("SELECT * FROM mood WHERE user_id = ?", (session['user_id'],))
    except Exception as e:
        # Handles the exception
        print(f"Error retrieving mood data: {e}")
        mood_data = []
     

    # Process mood data to extract relevant information for analytics
    dates = [entry.date for entry in mood_data]
    daily_moods = [entry.selected_mood for entry in mood_data]

    # Create a line chart using Matplotlib
    plt.plot(dates, daily_moods)
    plt.xlabel('Date')
    plt.ylabel('Daily Mood')
    plt.title('Mood Trends Over Time')
    plt.xticks(rotation=45)

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Convert the image to base64 for embedding in HTML
    img_base64 = base64.b64encode(img.getvalue()).decode()

    # Pass the base64-encoded image to the template
    return render_template('analytics.html', img_base64=img_base64)


# Error handler for all exceptions
@app.errorhandler(Exception)
def handle_error(e):
    print(f"An error occurred: {str(e)}")
    return apology("An Error Occurred", 403)

# Catch errors
if __name__ == '__main__':
    print("Reached app.run")
    app.run(debug=True)