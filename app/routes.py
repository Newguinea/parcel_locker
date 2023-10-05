# routes.py
from flask import render_template, flash, redirect, url_for, request
from werkzeug.exceptions import NotFound
from app import app
from app.models import User
from flask_login import login_required, LoginManager
from flask_login import current_user, login_user, logout_user
from app.models import Residence
from app import db
from flask import jsonify, make_response

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            # log user in
            return redirect(url_for('residence_list'))
        else:
            flash('Invalid username or password')
            # invalid login
            return redirect(url_for('login'))
    else:  # Handle GET request
        return render_template('login.html')


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


###############################################login above###############################################
@login_required
@app.route('/residences', methods=['POST'])
def create_residence():
    data = request.get_json()

    if not data:
        return jsonify({"error": {"message": "Invalid input", "code": 400}}), 400

    # Check if residence with same phone number already exists
    existing_residence = Residence.query.filter_by(phone_no=data['phone_no']).first()
    if existing_residence:
        return jsonify({"error": {"message": "A residence with this phone number already exists.", "code": 400}}), 400

    try:
        new_residence = Residence(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_no=data['phone_no'],
            unit_num=data['unit_num'],
            room_no=data['room_no'],
            nfc_id=data.get('nfc_id', None)
        )

        db.session.add(new_residence)
        db.session.commit()

        response = jsonify({'message': 'Residence created successfully'})
        return response, 201
    except Exception as e:
        return jsonify({"error": {"message": "Internal server error: " + str(e), "code": 500}}), 500


@login_required
@app.route('/residence_info_add')
def residence_info():
    return render_template('residence_info_add.html')


@login_required
@app.route('/residence_list')
def residence_list():
    return render_template('residence_list.html')


@login_required
@app.route('/residence_list_data')
def residence_list_data():
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

@login_required
@app.route('/delete_residence/<int:residence_id>', methods=['POST'])
def delete_residence(residence_id):
    """
    delete the residence with residence_id
    """
    try:
        residence = Residence.query.get_or_404(residence_id)
        db.session.delete(residence)
        db.session.commit()
        return '', 204  # No Content
    except NotFound:
        return jsonify({"error": {"message": "Residence not found", "code": 404}}), 404
    except Exception as e:
        return jsonify({"error": {"message": "Internal server error: " + str(e), "code": 500}}), 500

@login_required
@app.route('/edit_residence/<int:residence_id>', methods=['POST'])
def edit_residence(residence_id):
    """
    change the value of the residence with residence_id
    """
    residence = Residence.query.get_or_404(residence_id)
    data = request.get_json()

    # Check for phone number uniqueness
    existing_residence = Residence.query.filter_by(phone_no=data['phone_no']).first()
    if existing_residence and existing_residence.id != residence_id:
        return jsonify({"error": {"message": "A residence with this phone number already exists.", "code": 400}}), 400

    residence.first_name = data['first_name']
    residence.last_name = data['last_name']
    residence.email = data['email']
    residence.phone_no = data['phone_no']
    residence.unit_num = data['unit_num']
    residence.room_no = data['room_no']
    residence.nfc_id = data['nfc_id']

    try:
        db.session.commit()
        return jsonify({'message': 'Residence changed successfully'}), 200  # Use 200 OK for successful updates
    except Exception as e:
        return jsonify({"error": {"message": "Internal server error: " + str(e), "code": 500}}), 500


@login_required
@app.route('/residences/<int:residence_id>', methods=['GET'])
def get_residence(residence_id):
    """
    get all the information of the residence with residence_id
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
@app.route('/residence/<int:residence_id>', methods=['GET'])
def edit_residence_page(residence_id):
    return render_template('residence_info_edit.html', residence_id=residence_id)
