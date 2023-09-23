#models.py
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    hobby = db.Column(db.String(20), unique=True, nullable=False)
    # just a example