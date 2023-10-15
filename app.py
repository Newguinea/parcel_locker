#app.py
from app import app, db
from app.models import User
import threading
import PiLocker

if __name__ == "__main__":
    # Create and start PiLockerSystem
    pi_locker_system = PiLocker.PiLockerSystem()
    locker_thread = threading.Thread(target=pi_locker_system.start)
    locker_thread.start()

    app.run(host="0.0.0.0",debug=True)#run flask here
