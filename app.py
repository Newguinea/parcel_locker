#app.py
from app import app, db
from app.models import User
import threading
import time

def print_every_5_seconds():
    """print 1 in terminal every 5 seconds"""
    while True:
        print("1")
        time.sleep(5)

if __name__ == "__main__":
    """an example of running something and flask app at the same time"""
    t = threading.Thread(target=print_every_5_seconds)
    t.daemon = True  # Set the thread as a daemon thread to ensure it exits when the program exits.
    t.start()
    #flask app debug mode
    app.run(debug=True)
