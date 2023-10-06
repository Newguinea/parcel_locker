from flask_login import login_required
from app import app
from flask import jsonify, make_response
from app.models import Residence

@login_required
@app.route('/residences/<int:residence_id>', methods=['GET'])
def get_residence(residence_id):
    """
    get all the information of the residence with residence_id
    :param residence_id:
    :return format:
    {
        "data": {
            "email": "",
            "first_name": "",
            "last_name": "",
            "nfc_id": "",
            "phone_no": "",
            "room_no": "",
            "unit_num": ""
        },
        "message": "Success"
    }
    """
    residence = Residence.query.get_or_404(residence_id)
    return jsonify({
        'message': 'Success',
        'data': {
            'first_name': residence.first_name,
            'last_name': residence.last_name,
            'email': residence.email,
            'phone_no': residence.phone_no,
            'unit_num': residence.unit_num,
            'room_no': residence.room_no,
            'nfc_id': residence.nfc_id
        }
    }), 200


@login_required
@app.route('/residence_list_data')
def residence_list_data():
    """
    get all residence information about "name", "room_no", "email"
    :return format:
    {
        "data": [
            {
                "id": 1,
                "name": "John Doe",
                "room_no": "A1-01",
                "email": "instance1@instance1.com"
            },
            {
                "id": 2,
                "name": "Jane Doe",
                "room_no": "A1-02",
                "email": "instance2@instance2.com"
            }
        ],
        "message": "Success"
    }
    """
    try:
        residences = Residence.query.all()
        residence_list = []

        for residence in residences:
            residence_data = {
                'id': residence.id,
                'name': f"{residence.last_name} {residence.first_name}",
                'room_no': residence.room_no,
                'email': residence.email
            }
            residence_list.append(residence_data)

        return make_response(jsonify({
            "data": residence_list,
            "message": "Success"
        }), 200)

    except Exception as e:
        return make_response(jsonify({
            "error": {
                "message": str(e),
                "code": 500  # Internal Server Error
            }
        }), 500)
