#routes.py
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.models import User
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            # log user in
            return redirect(url_for('success'))
        else:
            # invalid login
            return redirect(url_for('hello_world'))
    else:  # Handle GET request
        return render_template('login.html')
@app.route('/success')
def success():
    return "Success"

@app.route('/hello_world')
def hello_world():
    return "Hello World"

@app.route("/")
def home():
    return "Hello, World!"
