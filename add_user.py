from app import app
from app import db
from app.models import User

import sys
print(sys.path)

with app.app_context():

    # Create a new User object
    new_user = User(username='aa', email='a@aa.com')

    # Set the user's password (this will hash it)
    new_user.password = 'aa'

    # Add the new User to the database session
    db.session.add(new_user)

    # Commit the transaction to the database
    db.session.commit()
