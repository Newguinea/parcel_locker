from app import app
from app import db
from app.models import User

#you can costomize the username, email and password here
username = "Zehua"
email = "23424251@student.uwa.edu.au"
password = "123456"

def main(username, email, password):
    """add a user to the database"""
    with app.app_context():
        # Check if a user with the same username already exists
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            print("Error: Username already exists!")
            return

        # Check if a user with the same email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print("Error: Email already exists!")
            return

        # Create a new User object
        new_user = User(username=username, email=email)

        # Set the user's password (this will hash it)
        new_user.password = password

        # Add the new User to the database session
        db.session.add(new_user)

        # Commit the transaction to the database
        db.session.commit()
        print("User successfully added to database")

if __name__ == "__main__":
    main(username, email, password)
