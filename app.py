#app.py
from app import app, db
from app.models import User
import threading
from hardware_connection.hardware import print_every_5_seconds

if __name__ == "__main__":
    """an example of running something and flask app at the same time"""
    t = threading.Thread(target=print_every_5_seconds)
    t.daemon = True  # Set the thread as a daemon thread to ensure it exits when the program exits.
    t.start()
    #flask app debug mode
    app.run(debug=True)
