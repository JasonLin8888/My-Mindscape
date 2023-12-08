
MyMindScape App Design Document

Overview

MyMindScape is a Flask-based web application designed to help users track and analyze their daily moods. The app provides a personalized dashboard where users can log their moods, record moments, and view analytics to understand mood trends over time. The design focuses on simplicity, user-friendly interfaces, and efficient data visualization.

Architecture

The app follows the Model-View-Controller (MVC) architectural pattern. The Flask framework is used to handle server-side logic, and the Jinja2 templating engine is employed for dynamic content generation. The app's data is stored in an SQLite database, mindscape.db and SQL from the CS50 library is used to execute transactions.

Frontend

The frontend utilizes HTML templates extended from a base layout. Bootstrap is incorporated to enhance the visual appeal and responsiveness of the user interface. The main templates include `index.html`, `dashboard.html`, `moment.html`, `analytics.html`, and `layout.html`. These templates provide a seamless and intuitive user experience.

Backend

The backend of the app is powered by Flask routes. Key routes include:

/home: Renders the user's personalized dashboard with options to record mood, view analytics, and display mood history.
/mood: Handles mood logging functionality, allowing users to select their mood, rate intensity, and add reflections.
/analytics: Generates mood analytics by processing and visualizing mood data over time.

Database Schema

The SQLite database contains tables for user information (`User`) and mood entries (`mood`). The `User` table stores user details, including their name, username, hashed password, and email. The `mood` table records individual mood entries with fields for user_id, id, mood_rating, selected_mood, intensity, date, and description.

Security

User passwords are securely hashed using the Werkzeug security library. Sessions are managed using Flask's built-in session handling. The app implements decorators like `login_required` to ensure secure access to routes that require authentication.

 Email Notification

The app incorporates email functionality for sending periodic mood summaries. Flask-Mail is used to compose and send HTML-formatted emails to users, providing insights into their weekly mood trends.

Error Handling

Error handling is implemented to gracefully manage unexpected situations. The app logs errors for future analysis and uses flash messages to provide users with meaningful feedback in case of invalid inputs or unexpected errors.

Future Improvements

Enhanced Analytics: Considering integrating more advanced data visualization libraries to provide users with deeper insights into their mood trends.
User Profile Settings: Implement functionality for users to customize their profiles, including profile pictures and notification preferences.
Mobile Responsiveness: Optimize the app for better user experience on mobile devices.

