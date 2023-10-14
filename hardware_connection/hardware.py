from app.models import Log
from email_module.mail import getrecipientinfo
from PiLocker import DoorControl


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
            'status': 'Success',
            'message': {
                'code': log.code,
                'nfc_id': log.nfc_id
            }
        }
    else:
        return {
            'status': 'Not_Found',
            'message': {
                'code': '',
                'nfc_id': ''
            }
        }
