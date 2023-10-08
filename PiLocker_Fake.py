# import PN532_UART as NFC
# from PiicoDev_QMC6310_new import PiicoDev_QMC6310
# from PiicoDev_SSD1306 import *
# from picamera import PiCamera
# import RPi.GPIO as GPIO

from time import sleep
from random import randint, choice
import string


# magSensor = PiicoDev_QMC6310(range=3000)
# threshold = 100 # microTesla or 'uT'.
# pn532 = NFC.PN532("/dev/ttyUSB0")
# display = create_PiicoDev_SSD1306()
# camera = PiCamera()



# magnet detection
def isLockerClosed():
    # while True:
    #     strength = magSensor.readMagnitude()
    #     strength_str = str(strength) + ' uT'
    #     print(strength_str)
    #     if strength > threshold:
    #         print('Strong Magnet! The locker is closed.')
    #         return True
    #     sleep(1)
    sleep(randint(1,5))
    return True


# nfc card uid reader
def getUID():
    # try:
    #     uid = pn532.read_passive_target(timeout=5000)
    #     uid = "".join("%02X" % i for i in uid)[:-1]
    #     return uid
    # except Exception as e:
    #     print(e)
    #     return "00000000"
    # except KeyboardInterrupt:
    #     pass
    characters = string.ascii_letters + string.digits
    random_uid = ''.join(choice(characters) for _ in range(8))
    return random_uid


# oled display
def sendToDisplay(text,line):
    # display.text(text, 0, 15*(line-1), 1)
    # display.show()
    return True


# camera
def takePhoto():
    # try:
    #     camera.capture('./image.jpg')
    #     return True
    # except Exception as e:
    #     print(e)
    #     return False
    return True
    

# relay
def openLocker():
    # try:
    #     GPIO.setmode(GPIO.BCM)
    #     relay_pin = 18
    #     GPIO.setup(relay_pin, GPIO.OUT)
    #     print("Locker opened")
    #     return True

    # except Exception:
    #     GPIO.cleanup()
    #     return False
    
    # finally:
    #     sleep(5)
    #     GPIO.cleanup()
    return True