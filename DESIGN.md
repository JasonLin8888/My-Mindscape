
MyMindscape App Design

Overview

The MyMindscape app is designed to provide users with a platform to record their daily moments and track their moods over time. Users can customize their profiles, including uploading profile pictures, and visualize their mood analytics through various features.

Technologies Used

Flask

This is a lightweight web framework for Python that was used to build the backend of the MyMindscape app. It handles routing, request handling, and integrates with other libraries.

CS50 Library

The CS50 library was used for database interactions instead of SQLAlchemy. It simplifies working with SQLite databases in a Flask application and was chosen for its simplicity and compatibility with the CS50 course.

Flask-Mail

Flask-Mail is a Flask extension for sending emails. It is used in the application to send periodic mood summaries to users.

Flask-Session

Flask-Session is an extension for managing user sessions in Flask applications. It is employed to keep track of user logins and ensure certain routes are accessible only to logged-in users.


Matplotlib

Matplotlib is a plotting library for Python. It is used to generate visualizations of mood analytics, providing users with insights into their mood trends over time.

Bootstrap

Bootstrap, a front-end framework, is used for styling the web pages. It ensures a responsive and visually appealing user interface.

 Features

User Authentication

Users can register, log in, and log out of the application. Authentication is handled securely, and passwords are hashed before storage.

Profile Customization

Users have the option to customize their profiles by providing a name, email, and uploading a profile picture.

Moment Recording

Users can record their daily moments by entering a date and a description. These moments are stored in the database for future reference.

Mood Tracking

Users can log their daily moods, indicating their mood and intensity. The application visualizes mood trends over time using Matplotlib.

Periodic Email Summaries

Flask-Mail is utilized to send periodic mood summaries to users, providing them with insights into their weekly mood trends.

Database Structure

The CS50 library is used to interact with the SQLite database. The main tables include:

User Table: Stores user information such as user ID, name, username, hashed password, and email.
  
Mood Table: Records daily moods, including user ID, mood type, intensity, and date.

Future Enhancements

1.Advanced Analytics: Incorporate more sophisticated analytics tools or machine learning models to provide users with deeper insights into their mood patterns.

2.User Settings: Expand user profile customization options, allowing users to update their information and preferences.

3.Improved Frontend: Enhance the user interface with more interactive elements and a modern design.

Conclusion

The MyMindscape app offers a user-friendly platform for individuals to reflect on their daily experiences and track their emotional well-being. The combination of Flask, CS50, and other libraries provides a robust foundation for future expansions and improvements.

