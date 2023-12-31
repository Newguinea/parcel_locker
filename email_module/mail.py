import requests
import datetime
import json
import sqlite3
import os
import random
import string
import base64
# from picamera import PiCamera
from dotenv import load_dotenv

# camera = PiCamera()
# camera.resolution = (320,240)

load_dotenv()
api_key = os.environ.get("API_KEY")

if not api_key:
    print("Error: API_KEY not found in environment variables")
    exit(1)


def getrecipientinfo(phoneNumber):
    """
    Get the recipient's information from the database.
    :param phoneNumber:
    :return format:
    {
        "status": "success",
        "first_name": "John",
        "email": ""
        nfc_id: ""
    }
    {
        "status": "failure",
        "message": "Phone number not found"
    }
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, '../app.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, email, nfc_id FROM residence WHERE phone_no=?", (phoneNumber,))
        row = cursor.fetchone()
        conn.close()

        output = {}
        if row:
            output['status'] = 'success'
            output['first_name'] = row[0]
            output['email'] = row[1]
            output['nfc_id'] = row[2]
        else:
            output['status'] = 'failure'
            output['message'] = 'Phone number not found'
        return json.dumps(output, indent=4)

    except sqlite3.Error as e:
        return json.dumps({"status": "failure", "message": f"Database error: {str(e)}"}, indent=4)


def notifyReceiveText(firstname, code):
    """
    Generate the text of the email to be sent to the recipient.
    :param name: The name of the recipient
    :return: The formatted text
    """
    # Get current time and format it
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format the text with variables
    text = f"""Dear {firstname},

Your package has been delivered and is now available for pick-up at our parcel locker location.

Use this pickup code: {code}

Time of Parcel Arrival:
{current_time}

If you need further assistance, please do not hesitate to contact us at 23424251@student.uwa.edu.au.

Thank you for using our services.

Best regards,
Smart Parcel locker
Customer Service Team
"""

    return text


def send_message(text, email_address, firstname):
    """
    Send the email to the recipient.
    :param text: the text of the email
    :param email_address:
    :param firstname:
    :return: {
        "status": "success",
        "message": "Email sent successfully"
    }
    """
    try:
        email_terminal = firstname + "<" + email_address + ">"
        result = requests.post(
            "https://api.mailgun.net/v3/vault.as4134.com/messages",
            auth=("api", api_key),
            data={"from": "Smart Parcel Locker <notify@vault.as4134.com>",
                  "to": email_terminal,
                  "subject": "You have a new parcel!",
                  "text": text})

        if result.status_code == 200:
            return {
                "status": "success",
                "message": "Email sent successfully"
            }
        else:
            return {
                "status": "failure",
                "message": f"Failed to send email: {result.text}"
            }

    except requests.RequestException as e:
        return {
            "status": "failure",
            "message": f"Failed to send email: {str(e)}"
        }


def getRandomcode4():
    """
    Generate a random 4-digit code.
    :return: The generated code
    """
    return ''.join(random.choice(string.digits) for _ in range(4))


def putLog(nfc_id, code, is_taken=False):
    """
    Put the log into the database.
    :param nfc_id:
    :param code:
    :param is_taken:
    :return:
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, '../app.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO log (nfc_id, code, timestamp, is_taken) VALUES (?, ?, ?, ?)",
                       (nfc_id, '0000', timestamp, is_taken))
        conn.commit()
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        return False


def sendPickupNotice(phoneNumber):
    """
    :param phoneNumber:
    :return:
    a json format data
    {
        "status": "success",
        "code": 1234,
        "nfc_id": "12345678"
    }
    {
        "status": "failure",
        "message": "Phone number not found"
    }
    """
    recipientinfo = getrecipientinfo(phoneNumber)
    recipientinfo = json.loads(recipientinfo)

    if recipientinfo['status'] == 'success':
        firstname = recipientinfo['first_name']
        email = recipientinfo['email']
        nfc_id = recipientinfo['nfc_id']
        code = getRandomcode4()
        text = notifyReceiveText(firstname, code)
        result = send_message(text, email, firstname)
        putLog(nfc_id, code, is_taken=False)
        if result['status'] == 'success':
            return json.dumps({"status": "success", "code": code, "nfc_id": nfc_id}, indent=4)
        else:
            return json.dumps(result, indent=4)

    elif recipientinfo['status'] == 'failure':
        return json.dumps(recipientinfo, indent=4)  # return the error message


def read_image(file_path):
    with open(file_path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


def send_email_with_mailgun(receiver_email, file_path):

    image_data = read_image(file_path)

    html = f"""
    <html>
    <head></head>
    <body>
    <p>We have detected suspicious behavior on the security camera. Please take appropriate action immediately.</p>
    <p><img src="data:image/jpeg;base64,{image_data}" alt="pic"></p>
    </body>
    </html>
    """
    return requests.post(
        f"https://api.mailgun.net/v3/vault.as4134.com/messages",
        auth=("api", api_key),
        data={"from": "Smart Parcel Locker <notify@vault.as4134.com>",
              "to": receiver_email,
              "subject": "Suspicious Behavior Detected",
              "html": html})

if __name__ == '__main__':
    # print(getrecipientinfo("0466628549"))
    camera.capture("/home/iot-lab-2023/cits5506/1.jpg", quality=2)
    send_email_with_mailgun("rfc@live.com", "/home/iot-lab-2023/cits5506/1.jpg")
