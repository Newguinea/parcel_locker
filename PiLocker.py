import PN532_UART as NFC
from PiicoDev_QMC6310_new import PiicoDev_QMC6310
from PiicoDev_SSD1306 import *
from picamera import PiCamera
import RPi.GPIO as GPIO

from time import sleep
from  hardware_connection.hardware import getLastUserCode

magSensor = PiicoDev_QMC6310(range=3000)
threshold = 100 # microTesla or 'uT'.
pn532 = NFC.PN532("/dev/ttyUSB0")
display = create_PiicoDev_SSD1306()
camera = PiCamera()


class Hardware:
    #variables
    def __init__(self):
        self.door_status = False
    # magnet detection
    def isLockerClosed(self):
        """
        every 5 seconds, check if the magnet is detected
        :param threshold:
        :param magSensor:
        if the magnet is detected, return True
        else, return False
        :return:
        """
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
            sleep(1)


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