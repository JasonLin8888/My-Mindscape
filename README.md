MyMindScape

MyMindScape is a web application that allows users to track their mood and record moments in a personal diary. This README provides a user's manual for the application.

Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

Installation

1. Clone the repository:

   bash
   git clone https://github.com/JasonLin8888/My-Mindscape
   

2. Navigate to the project directory:

   bash
   cd MyMindScape
   

3. Install the required dependencies:

   bash
   pip install -r requirements.txt
 

4. Set up the configuration file:

   - Create a `.env` file in the project root.
   - Add the following environment variables:

     plaintext
     FLASK_APP=app.py
     FLASK_ENV=development
     

5. Initialize the database:

   bash
   flask db init
   flask db migrate
   flask db upgrade
   

Usage

1. Run the application:

   bash
   flask run
   

2. Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

3. Register for a new account or log in if you already have one.

4. Explore the different features of MyMindScape, including recording moments, tracking mood, and viewing analytics.

Features

- Record Moments: Document your thoughts and experiences by recording moments with descriptions and dates.

- Track Mood: Log your daily mood and intensity to keep track of your emotional well-being.

- Analytics:Visualize your mood trends over time with interactive charts.

- Profile Picture: Customize your profile by uploading a profile picture.

Dependencies

- Flask: Web framework for Python
- SQLite: Database engine
- Flask-Mail: Email sending in Flask
- Flask-Session: Extension for server-side session management
- Flask-Migrate: Database migration with Flask
- Matplotlib: Data visualization library
- Bootstrap: Front-end framework
- Chart.js: JavaScript charting library

Contributing

If you would like to contribute to MyMindScape, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.

License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


