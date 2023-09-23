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

### Running the Application

To run the application, execute:

```bash
flask run
```

Visit `http://localhost:5000` in your web browser to view the application.