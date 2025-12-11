TaskVault

TaskVault is a modular Flask-based task-management application designed for clarity, scalability, and ease of use. It provides a clean structure for learning, extending, or deploying small-to-medium Flask projects.

Features

Create, update, and delete tasks.

Organized project architecture:

Modular route system (routes/)

Template-driven UI (templates/)

Clean models with SQLAlchemy (models.py)

Database migrations using Flask-Migrate.

Easy to extend with authentication, categories, priorities, or APIs.

Fully configurable and ready for hosting.

Project Structure
taskvault/
│
├── app.py               # Flask application factory
├── run.py               # Main entry point
├── models.py            # SQLAlchemy models
├── routes/              # Modular routing system
├── templates/           # HTML templates (Jinja2)
├── migrations/          # Flask-Migrate files
├── requirements.txt     # All dependencies
└── instance/ (created automatically at runtime)

How to Install and Run the Project
1. Create a Virtual Environment
python -m venv venv

2. Activate the Environment

Windows:

venv\Scripts\activate


Linux / macOS:

source venv/bin/activate

3. Install All Required Libraries
pip install -r requirements.txt

4. Create the Instance Folder

If it does not exist:

mkdir instance

5. Initialize the Database

Run migrations:

flask db init
flask db migrate
flask db upgrade


This will create the SQLite database inside instance/.

6. Run the Application
python run.py

7. Access the App

Open your browser:

http://127.0.0.1:5000


Your TaskVault web app is now running.
