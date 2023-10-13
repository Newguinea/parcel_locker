## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. Python 3.11
2. pip
3. virtualenv

### Installation Steps

#### Clone the repository

```bash
git clone https://github.com/JoelQian/cits5506.git
cd cits5506
```

#### Setup Virtual Environment (Optional but Recommended)

It's often best to run Python code in a virtual environment to manage dependencies. If you haven't installed `virtualenv` yet, you can install it with:

```bash
pip install virtualenv
```

Create a virtual environment and activate it:

For Windows:
```bash
virtualenv venv
.\venv\Scripts\activate
```

For macOS and Linux:
```bash
virtualenv venv
source venv/bin/activate
```

#### Install Required Packages

Install the packages required for this project by running:

```bash
pip install -r requirements.txt
```

### Database Initialization
Before running the application, you need to initialize, migrate, and upgrade the database using Flask-Migrate. If you haven't set up Flask-Migrate, ensure it's installed by checking your requirements.txt or installing it directly with pip.

To set up the database, follow these steps:
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

```

These three commands will:

1. Initialize a new migration repository.
2. Autogenerate a new migration script, detailing the changes to be applied to the database.
3. Apply these changes to the database.

### Add administer to database
run add_user.py add a administer account to database. you can change the account name, email, password in the file.

```bash
python add_user.py
```

### Running the Application

To run the application, in the root of the folder execute:

```bash
python app.py
```

Visit `http://localhost:5000` in your web browser to view the application.

## Email module
the key of emailgun is in .env file, you can change it to your own key.

## Running the Tests

To ensure that the application is functioning as expected, a comprehensive suite of unit tests has been included. These tests cover everything from user authentication to CRUD operations for residences and API endpoints.

### Running Unit Tests

1. Navigate to the project root directory in your terminal.
2. Execute the following command to run the tests:

```shell
python -m unittest tests/tests.py
```
This command will search for all tests in the project and run them. Upon completion, a summary of the tests will be displayed, including any failures or errors.

It's recommended to run these tests frequently during development to catch any potential issues early on.

## Built With

* [Flask](http://flask.palletsprojects.com/) - The web framework used.
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - An extension for Flask that simplifies database operations using SQLAlchemy.
* [Flask-Migrate](https://flask-migrate.readthedocs.io/) - An extension for Flask that handles SQLAlchemy database migrations for Flask applications using Alembic.
* [SQLite](https://www.sqlite.org/) - Lightweight database used for testing purposes.
* [unittest](https://docs.python.org/3/library/unittest.html) - The standard library for building and running tests in Python.
