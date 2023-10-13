import unittest
import json
from app import app, db
from app.models import User,Residence
from unittest.mock import patch


class RoutesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        #create the db
        with app.app_context():
            db.create_all()
            db.session.add(User(username='test', email='test@test.com', password='test'))
            db.session.commit()

    def tearDown(self) -> None:
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        self.app.post('/login', data=dict(username='testuser', password='testpassword'), follow_redirects=True)

    def test_login(self):
        response = self.app.post('/login', data=dict(username='test', email='test@test.com', password='test'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Resident List', response.data)

    def test_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_create_residence(self):
        # Log in first since the route requires authentication
        self.login()

        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@test.com",
            "phone_no": "1234567890",
            "unit_num": "A101",
            "room_no": "1A",
            "nfc_id": "nfc12345"
        }

        response = self.app.post('/residences', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Residence created successfully', response.data)


    def test_delete_residence(self):
        # Log in first since the route requires authentication
        self.login()

        with app.app_context():
            # Creating a residence to delete later
            residence = Residence(first_name='Alice', last_name='Brown', email='alice.brown@test.com',
                                  phone_no='0112233445',
                                  unit_num='C303', room_no='3C', nfc_id='nfc67890')
            db.session.add(residence)
            db.session.commit()

            response = self.app.post(f'/delete_residence/{residence.id}')

        self.assertEqual(response.status_code, 204)  # No Content

    def test_edit_residence(self):
        # Log in first since the route requires authentication
        self.login()

        edited_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@test.com",
            "phone_no": "0987654322",
            "unit_num": "B203",
            "room_no": "2C",
            "nfc_id": "nfc54322"
        }

        with app.app_context():
            # Creating a residence to edit later
            residence = Residence(first_name='Jane', last_name='Doe', email='jane.doe@test.com', phone_no='0987654321',
                                  unit_num='B202', room_no='2B', nfc_id='nfc54321')
            db.session.add(residence)
            db.session.commit()

            response = self.app.post(f'/edit_residence/{residence.id}', json=edited_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Residence changed successfully', response.data)

class APITestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        #create the db
        with app.app_context():
            db.create_all()
            db.session.add(User(username='test', email='test@test.com', password='test'))
            db.session.commit()

    def tearDown(self) -> None:
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        self.app.post('/login', data=dict(username='testuser', password='testpassword'), follow_redirects=True)


    def test_get_residence(self):
        self.login()  # Ensure you're logged in

        # Creating a residence to fetch later
        with app.app_context():
            residence = Residence(first_name='John', last_name='Doe', email='john.doe@test.com', phone_no='0123456789',
                                  unit_num='A101', room_no='1A', nfc_id='nfc12345')
            db.session.add(residence)
            db.session.commit()

            response = self.app.get(f'/residences/{residence.id}')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Success')
            self.assertEqual(data['data']['first_name'], 'John')

    def test_residence_list_data(self):
        self.login()

        # Creating a couple of residences
        with app.app_context():
            residence1 = Residence(first_name='John', last_name='Doe', email='john.doe@test.com', phone_no='0123456789',
                                   unit_num='A101', room_no='1A', nfc_id='nfc12345')
            residence2 = Residence(first_name='Jane', last_name='Smith', email='jane.smith@test.com', phone_no='9876543210',
                                   unit_num='B102', room_no='2B', nfc_id='nfc54321')
            db.session.add_all([residence1, residence2])
            db.session.commit()

            response = self.app.get('/residence_list_data')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Success')
            self.assertEqual(len(data['data']), 2)

    def test_getNFCID_success(self):
        self.login()

        with patch('app.api.getUID', return_value="12345678"):
            response = self.app.get('/getNFCID')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['NFCid'], '12345678')

    def test_getNFCID_error(self):
        self.login()

        # Test for NFCid = "00000000"
        with patch('app.api.getUID', return_value="00000000"):
            response = self.app.get('/getNFCID')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 500)
            self.assertEqual(data['status'], 'failure')
            self.assertEqual(data['message'], 'Error')

        # Test for NFCid = None
        with patch('app.api.getUID', return_value=None):
            response = self.app.get('/getNFCID')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 500)
            self.assertEqual(data['status'], 'failure')
            self.assertEqual(data['message'], 'Error')