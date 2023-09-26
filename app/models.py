#models.py
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)

class Residence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    room_no = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    unit_num = db.Column(db.Integer, nullable=False)
    nfc_id = db.Column(db.String(100))