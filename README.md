MyMindscape Project

Youtube Link: https://youtu.be/c880dVYMAi4

Introduction

Welcome to Mindscape, a web application designed to help users track and reflect on their daily moments and moods. This documentation serves as a user's manual, providing clear instructions on how to compile, configure, and use the Mindscape project. Whether you're a new user looking to get started or a developer exploring the project structure, this guide will help you navigate through the application.

Getting Started

Prerequisites

- Ensure you have Python installed on your machine. If not, you can download it from [python.org](https://www.python.org/).
- Install the required Python packages by running the following command in the project directory:

    ```bash
    pip install -r requirements.txt
    ```

 Configuration

1. Open the `config.py` file in the project directory.

2. Set your Gmail credentials for sending email notifications:

    ```python
    MAIL_USERNAME = 'YourGmail@gmail.com'  # replace with your Gmail email
    MAIL_PASSWORD = 'YourGmailPassword'    # replace with your Gmail password
    ```

3. Configure the database URI in the same file:

    ```python
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mindscape.db'
    ```

Running the Application

1. In the terminal, navigate to the project directory.

2. Run the following command to initialize the Flask application:

    ```bash
    flask run
    ```

3. Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to access the Mindscape application.

 Usage

 Registering a New Account

1. Click on the "Register" link on the navigation bar.

2. Fill in the registration form with your name, username, password, password confirmation, and email.

3. Click the "Register" button to create a new account.

 Logging In

1. Click on the "Login" link on the navigation bar.

2. Enter your username and password.

3. Click the "Login" button to access your account.

 Recording Moments

1. Once logged in, click on the "Moment" link on the navigation bar.

2. Fill in the form with the date and description of your moment.

3. Click the "Record Moment" button to save the moment.

Tracking Mood

1. Click on the "Mood" link on the navigation bar.

2. Select your mood, set the intensity, and choose the date.

3. Click the "Record Mood" button to track your mood.

 Viewing Analytics

1. Click on the "Analytics" link on the navigation bar.

2. Explore the interactive charts to gain insights into your mood trends over time.

Logging Out

1. To log out, click on the "Logout" link on the navigation bar.

 Additional Information

- The application sends periodic mood summaries to the registered email address. Ensure that the configured Gmail credentials are accurate for email functionality.

- For any technical issues or errors, refer to the `logs` folder for detailed error logs.

- If you encounter any problems, feel free to reach out to the project developer.

Thank you for using MyMindscape! We hope this user's manual makes your experience with the application enjoyable and insightful.