from app.models import Log
import os
import sqlite3
import json

def getLastUserCode():
    """
    Get the latest unclaimed code from the Log table.

    :return format:
    {
        "status": "Success",
        "message": {
            "code": "12345678",
            "nfc_id": "12345678"
        }
    }
    {
        "status": "Not_Found",
        "message": {
            "code": "",
            "nfc_id": ""
        }
    }
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, '../app.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT code, nfc_id FROM Log WHERE is_taken=0 ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'status': 'Success',
                'message': {
                    'code': row[0],
                    'nfc_id': row[1]
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

    except sqlite3.Error as e:
        return json.dumps({"status": "failure", "message": f"Database error: {str(e)}"}, indent=4)