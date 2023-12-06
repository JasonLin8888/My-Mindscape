from flask import Flask, render_template, request, redirect, url_for, session, flash
from helpers import login_required, logout_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta
from flask_mail import Message, Mail
from io import BytesIO
import os
import bcrypt
import re
import matplotlib.pyplot as plt
import base64


app = Flask(__name__)
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # or 587
app.config['MAIL_USE_SSL'] = True  # or False
app.config['MAIL_USE_TLS'] = False  # or True
app.config['MAIL_USERNAME'] = 'MyMindScape@gmail.com'  # your email
app.config['MAIL_PASSWORD'] = 'Copyright@Ian&Jason'  # your email password
app.config['MAIL_DEFAULT_SENDER'] = 'MyMindScape@gmail.com'
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
    intensity = db.Column(db.Integer, nullable=False)
    selected_mood = db.Column(db.String(20), nullable=False)
    reflection = db.Column(db.Text, nullable=False)
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
    return render_template('registration.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
@logout_required  # Use the helper decorator to ensure the user is not logged in
def login():
    #Check if the user is already logged in
    if session.get('user_id'):
        # If the user is already logged in, redirect to the home page
        return render_template(('home'))
        # If the request method is POST, process the form data
        
    if request.method == 'POST':
        # Process login form data here
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if username and password were provided
        if not username or not password:
            flash('Please provide both username and password', '400')
            return render_template('login.html')

        # Retrieve the user object from the database
        user = User.query.filter_by(username=username).first()

        # Hash the password and check
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            session['user_id'] = user.user_id
            flash('Login successful!', '200')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', '400')
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
@app.route('/moment', methods=['GET', 'POST'])
@login_required  # Use the helper decorator to ensure the user is logged in
def record_moment():
   # get input from the form and record it in the mood table in the database
    if request.method == 'POST':
        # Process the form data here
        date = request.form['date']
        description = request.form['description']
        # Create a new entry object using the form data
        new_entry = mood(user_id=session['user_id'], date=date, description=description)
        # Add the new entry to the database
        db.session.add(new_entry)
        db.session.commit()
        # Redirect to the home page after successful login
        return redirect(url_for('home'))
    # Render the record moment page if it's a GET request
    return render_template('record_moment.html')

# Define the route to  mood
@app.route('/mood', methods=['POST'])
@login_required  # Ensure the user is logged in
def mood():
    if request.method == 'POST':
        # Retrieve the mood and intensity values from the form submission
        selected_mood = request.form['mood']
        intensity = int(request.form['intensity'])

        # Perform any necessary processing or validation

        # Create a new mood entry in the database
        new_entry = mood(user_id=session['user_id'], mood=selected_mood, intensity=intensity, date=datetime.now())
        db.session.add(new_entry)
        db.session.commit()

        # Redirect to the home page or another appropriate page
        return redirect(url_for('home'))


@app.route('/analytics')
@login_required
def analytics():
    # Retrieve the user's mood data from the database
    user_id = session['user_id']
    mood_data = mood.query.filter_by(user_id=user_id).all()

    # Process mood data to extract relevant information for analytics
    dates = [entry.date for entry in mood_data]
    daily_moods = [entry.daily_mood for entry in mood_data]

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

@app.route('/dashboard')
@login_required
def dashboard():
    # Retrieve the user's mood history from the database
    user_id = session['user_id']
    mood_history = mood.query.filter_by(user_id=user_id).order_by(mood.date.desc()).limit(10).all()

    # Pass the mood data to the template
    return render_template('dashboard.html', mood_history=mood_history)

# define function get_mood_data_for_period
def get_mood_data_for_period(user_id, period):
    # Retrieve the user's mood data from the database
    mood_data = mood.query.filter_by(user_id=user_id).all()

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

# define function format_mood_summary
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

    #create a funtion to send email, using flask mail, body should be formatted summary, and title should be weekly mood summary

# define function send_email

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
    


# Route for sending periodic summaries
@app.route('/send_periodic_summary', methods=['GET'])
@login_required
def send_periodic_summary():
    # Assuming you have a function to get mood data for the past week or month
    mood_data = get_mood_data_for_period(session['user_id'], 'week')  # You need to implement this function

    # Assuming you have a function to format mood data for display
    formatted_summary = format_mood_summary(mood_data)  # You need to implement this function

    # Assuming you have a function to send an email using Flask-Mail
    send_email(session['user_email'], 'Weekly Mood Summary', formatted_summary)  # You need to implement this function

    return "Periodic summary sent successfully!"

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # You might want to log the error or handle it appropriately
        render_template('apology.html', message='An error occurred')

