#app.py
from app import app, db
from app.models import User
import threading
from PiLocker import DoorControl, PiLockerSystem

if __name__ == "__main__":
    # Create and start PiLockerSystem
    pi_locker_system = PiLockerSystem()
    locker_thread = threading.Thread(target=pi_locker_system.start)
    locker_thread.start()

    app.run(debug=True)#run flask here
