import requests as requests
import datetime
import json
import sqlite3
import os

def getrecipientinfo(phoneNumber):
    """
    Retrieve the first name and email associated with a given phone number from the database.

    :param str phoneNumber: The phone number to search for in the database.
    :return: A JSON object containing either the successful output with the first name and email,
             or a failure message if the phone number is not found.
    :rtype: json
    """
    # get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, '../app.db')

    # connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # execute the query
    cursor.execute("SELECT first_name, email FROM residence WHERE phone_no=?", (phoneNumber,))

    # got the result
    row = cursor.fetchone()

    # close the connection
    conn.close()

    output = {}
    if row:
        output['status'] = 'success'
        output['first_name'] = row[0]
        output['email'] = row[1]
    else:
        output['status'] = 'failure'
        output['message'] = 'Phone number not found'

    return json.dumps(output, indent=4)

def genText(firstname):
    """
    Generate the text of the email to be sent to the recipient.
    :param name: The name of the recipient
    :return: The formatted text
    """
    # Get current time and format it
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format the text with variables
    text = f"""Dear {firstname},

We are pleased to inform you that a package has been delivered and is now available for pick-up at our parcel locker location.

Time of Parcel Arrival:
{current_time}

Please ensure to collect your package within the specified time window. Failure to do so may result in the package being returned to the sender.

To retrieve your package, you'll need to provide valid identification that matches the name on the package.

If you have any questions or require further assistance, please do not hesitate to contact us at 23424251@student.uwa.edu.au.

Thank you for using our services.

Best regards,
Smart Parcel locker
Customer Service Team
"""

    return text

def send_message(text, email_address, firstname):
    """
    :param text: the main body of the email
    :param email_address: format: "23424251@student.uwa.edu.au"
    :return:
    <Response [200]> for success
    others for failure
    """
    email_terminal = firstname + "<" + email_address + ">"
    result = requests.post(
        "https://api.mailgun.net/v3/sandbox9fdc432bf42b4f54b4a0ec5582a80102.mailgun.org/messages",
        auth=("api", "0659ac7fa6d863191bcf2bc65de68b17-77316142-96a02996"),
        data={"from": "smart-locker-box <notification.noreply@smart-locker-box.com>",
            "to": email_terminal,
            "subject": "You have a new parcel in box",
            "text": text})
    return str(result)

def main(phoneNumber):
    #get the recipient info
    recipientinfo = getrecipientinfo(phoneNumber)
    #parse the json
    recipientinfo = json.loads(recipientinfo)
    #check if the phone number is found
    if recipientinfo['status'] == 'success':
        #get the first name and email
        firstname = recipientinfo['first_name']
        email = recipientinfo['email']
        #generate the text
        text = genText(firstname)
        #send the message
        result = send_message(text, email, firstname)
        print(result)
    else:
        print(recipientinfo['message'])


if __name__ == '__main__':
    main("0466628549")