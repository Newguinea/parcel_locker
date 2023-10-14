# PiLocker.py
import PN532_UART as NFC
from PiicoDev_QMC6310_new import PiicoDev_QMC6310
from PiicoDev_SSD1306 import *
from picamera import PiCamera
import RPi.GPIO as GPIO
import threading
import time
from time import sleep
from hardware_connection.hardware import getLastUserCode
from email_module.mail import getrecipientinfo
import queue

magSensor = PiicoDev_QMC6310(range=3000)
threshold = 100 # microTesla or 'uT'.
pn532 = NFC.PN532("/dev/ttyUSB0")
display = create_PiicoDev_SSD1306()
camera = PiCamera()


class DoorControl:
    #variables
    def __init__(self):
        self.door_status = False#door is open or not True for open, False for close
        self.box_is_empty = True#box is open or not
    # magnet detection
    def isLockerClosed(self):
        """
        check the door is closed or not
        :param threshold:
        :param magSensor:
        if the magnet is detected, return True
        else, return False
        :return:
        """
        sleep(7000)
        while True:
            strength = magSensor.readMagnitude()
            strength_str = str(strength) + ' uT'
            print(strength_str)
            if strength > threshold:
                print('Strong Magnet! The locker is closed.')
                self.door_status = True
                return True
            else:
                print('The locker is open.')
                self.door_status = False
                return False

    # relay
    def openLocker(self):
        try:
            GPIO.setmode(GPIO.BCM)
            relay_pin = 18
            GPIO.setup(relay_pin, GPIO.OUT)
            print("Locker opened")
            self.door_status = True
            return True

        except Exception:
            GPIO.cleanup()
            return False

        finally:
            sleep(5)
            GPIO.cleanup()

    def runSensor(self):
        """run isLockerClosed function in a thread, 5 seconds per loop"""
        while True:
            self.isLockerClosed()
            print(f"Current magnetic strength: {self.door_status} uT")
            time.sleep(5)

    def set_box_is_empty(self):
        self.box_is_empty = True

    def set_box_is_not_empty(self):
        self.box_is_empty = False



class PiLockerSystem:
    def __init__(self):
        self.hardware = DoorControl()
        self.thread = threading.Thread(target=self.hardware.runSensor)
        self.thread.start()

    def start(self):
        while True:
            # no things in the box
            if self.hardware.box_is_empty == True:
                if self.hardware.door_status == False:
                    # deliveryman put the parcel into the box
                    self.sendToDisplay("please input phone number", 1)
                    mobileInput = self.pinpadMobile()
                    #check the mobile number is in the database or not
                    checkReceiver = getrecipientinfo(mobileInput)
                    if checkReceiver['status'] == 'success':
                        self.hardware.openLocker()
                        self.sendToDisplay("please close the door when finised", 1)
                        self.hardware.box_is_empty = False
                        # use isLockerClosed function to check the door is closed or not
                        while True:
                            if self.hardware.isLockerClosed() == True:
                                self.hardware.set_box_is_not_empty()
                                break
                            else:
                                self.hardware.set_box_is_empty()
                                break
                    elif checkReceiver['status'] == 'failure':
                        self.sendToDisplay(checkReceiver['message'], 1)

                    self.sendToDisplay("please lock the door", 1)
                    sleep(5)
                elif self.hardware.door_status == True:
                    #TODO door was not closed properly
                    self.sendToDisplay("please close the door", 1)
                    sleep(5)
            # things in the box(user pick up the parcel)
            elif self.hardware.box_is_empty == False:
                if self.hardware.door_status == False:
                    #user pick up the parcel
                    self.sendToDisplay("please input the code to unlock the door or use nfc tag", 1)
                    self.waitForUnlock()

                elif self.hardware.door_status == True:
                    #user did not pick up the parcel
                    self.sendToDisplay("please pick up the things in box", 1)
                    sleep(5)

    def waitForUnlock(self):
        q = queue.Queue()
        t1 = threading.Thread(target=self.getNFCInput, args=(q,))
        t2 = threading.Thread(target=self.getPinpadInput, args=(q,))
        t1.start()
        t2.start()

        source, value = q.get()  # when there is no data in the queue, it will block the thread
        if source == 'nfc':
            # if value is same as getLastUserCode
            if value == getLastUserCode()['message']['nfc_id']:
                self.hardware.openLocker()
                self.sendToDisplay("please close the door when finised", 2)
                self.hardware.box_is_empty = True
                sleep(5)
            else:
                self.sendToDisplay("wrong nfc tag", 1)
                sleep(5)
        else:
            # if value is same as getLastUserCode
            if value == getLastUserCode()['message']['code']:
                self.hardware.openLocker()
                self.sendToDisplay("please close the door when finised", 2)
                self.hardware.box_is_empty = True
                sleep(5)
            else:
                self.sendToDisplay("wrong code", 1)
                sleep(5)


    # nfc card uid reader
    def getUID(self):
        """
        read the uid of the nfc card
        :return:
        """
        try:
            uid = pn532.read_passive_target(timeout=5000)
            uid = "".join("%02X" % i for i in uid)[:-1]
            return uid
        except Exception as e:
            print(e)
            return "00000000"
        # TODO: why here has a KeyboardInterrupt?
        except KeyboardInterrupt:
            pass


    # oled display
    def sendToDisplay(text,line):
        """
        display the text on the oled screen(128x64 pixels),(4 lines, 16 characters per line)
        :param text: the text to be displayed
        :param line: 1-4
        will display the text on the line of the oled screen
        the number of line is from 1 to 8
        """
        # clear the screen
        display.clear()
        # display.fill(0)
        display.text(text, 0, 15*(line-1), 1)
        display.show()


    # camera
    def takePhoto(self):
        try:
            camera.capture('./image.jpg')
            return True
        except Exception as e:
            print(e)
            return False


    def pinpadCode(self):
        """
        TODO: get the input from the pinpad
        :return: 4-digit pin
        """
        code = input("Please enter your pin: ")
        return code

    def pinpadMobile(self):
        """"""
        mobile = input("Please enter your mobile: ")
        return mobile