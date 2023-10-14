#app.py
from app import app, db
from app.models import User
import threading
from PiLocker import DoorControl, PiLockerSystem

# hardware_instance = None  # global variable
# """
# example of get value of global variable
#
# import app
# status = app.hardware_instance.door_status
# print("Door status:", status)
# """

# def startHallSensorInThread():
#     """start the hall sensor in a thread"""
#     global hardware_instance
#     hardware = DoorControl()
#     thread = threading.Thread(target=hardware.runSensor)
#     thread.start()
#     hardware_instance = hardware
#     return hardware


if __name__ == "__main__":
    # sensor_instance = startHallSensorInThread()

    # Create and start PiLockerSystem
    pi_locker_system = PiLockerSystem()
    pi_locker_system.start()

    app.run(debug=True)#run flask here
