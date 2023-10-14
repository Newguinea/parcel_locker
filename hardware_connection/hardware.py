import time
from app.models import Log
from email_module.mail import sendPickupNotice
from PiLocker import Hardware
def print_every_5_seconds():
    """print 1 in terminal every 5 seconds"""
    while True:
        print("1")
        time.sleep(5)


def getLastUserCode():
    """get the data from Log table, is_taken = 0,timestamp is the latest
    return a dict
    {
    code: "Success"
    message: {
            "code": "12345678",
            "nfc_id": "12345678"
        }
    }
    """

    log = Log.query.filter_by(is_taken=0).order_by(Log.timestamp.desc()).first()
    if log:
        return {
            'code': 'Success',
            'message': {
                'code': log.code,
                'nfc_id': log.nfc_id
            }
        }
    else:
        return {
            'code': 'Not_Found',
            'message': {
                'code': '',
                'nfc_id': ''
            }
        }

def putIteamToBox(mobile):
    returnValue = sendPickupNotice(mobile)
    if returnValue['status'] == 'success':
        Hardware.sendToDisplay('Succeed', 1)
        #TODO screen show succeed

    elif returnValue['status'] == 'failure':
        Hardware.sendToDisplay(returnValue['message'], 1)
        #TODO screen message in the screen