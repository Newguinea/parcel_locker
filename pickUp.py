import os
import sqlite3
import json

def getMostRecentRecords():
    """get most recent(latest) records from log table,
    return
        {
            nfc_id: nfc_id,
            code: code,
            id: id
        }
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, './app.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT nfc_id, code, id FROM log WHERE is_taken=0 ORDER BY timestamp DESC LIMIT 1")

        row = cursor.fetchone()
        conn.close()

        output = {}
        if row:
            output['nfc_id'] = row[0]
            output['code'] = row[1]
            output['id'] = row[2]
        else:
            output['nfc_id'] = '00000000'
            output['code'] = 0
        return json.dumps(output, indent=4)

    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        return {"nfc_id": "00000000", "code": 0}
    return {"nfc_id": "00000000", "code": 0}

def setParcelis_taken(id):
    """set is_taken to True in log table"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, './app.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE log SET is_taken = 1 WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        return False
    return False

def checkNFC(read_nfc_id,nfc_id):
    """check the nfc input and compare with the nfc_id in Log,
    if same return True, else return False
    """
    return read_nfc_id == nfc_id

def checkCode(read_code,code):
    """check the code input and compare with the code in Log,
    if same return True, else return False
    """
    return read_code == code

def main():
    # data from database
    parcelinfo = getMostRecentRecords()
    parcelinfo = json.loads(parcelinfo)
    id = parcelinfo['id']
    nfc_id = parcelinfo['nfc_id']
    code = parcelinfo['code']

    #data from the user and NFC tag(fake data)
    read_nfc_id = "00000000"
    read_code = 8989

    if checkNFC(read_nfc_id,nfc_id) and checkCode(read_code,code):
        # open the locker and change the data in database
        setParcelis_taken(id)# set is taken to "1"(true)
        #TODO: open the locker
        return True
    else:
        return False

if __name__ == "__main__":
    print(getMostRecentRecords())