import unittest
from app import create_app
from custom_exceptions import *
from extensions import db

from methods import JWTToken, Restricted
from models.user import User


class TestMethods(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_class="config.config_testing")
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.populate_db()
        self.jwt_token = JWTToken()
        self.protected = Restricted()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None
        self.jwt_token = None
        self.protected = None

    def populate_db(self):
        user = User(username='admin',
                    password='15e24a16abfc4eef5faeb806e903f78b188c30e4984a03be4c243312f198d1229ae8759e98993464cf713e3683e891fb3f04fbda9cc40f20a07a58ff4bb00788',
                    role='admin',
                    salt='F^S%QljSfV')
        db.session.add(user)
        db.session.commit()

    def test_generate_token(self):
        self.assertEqual('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI',
                         self.jwt_token.generate_token('admin'))

    def test_access_data(self):
        self.assertEqual(True, self.protected.has_access_data(
            'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI'))

    def test_login_with_correct_username_and_password(self):
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'secret',
        })

        self.assertEqual(200, response.status_code)

    def test_login_with_incorrect_password(self):
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'secretv',
        })

        self.assertEqual(403, response.status_code)

    def test_login_with_incorrect_user(self):
        response = self.client.post('/login', data={
            'username': 'admiin',
            'password': 'secret',
        })

        self.assertEqual(403, response.status_code)

    def test_protected_url_with_valid_token(self):
        response = self.client.get(
            '/protected',
            headers={
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI'
            }
        )

        self.assertEqual(200, response.status_code)

    def test_protected_url_without_bearer(self):
        response = self.client.get(
            '/protected',
            headers={
                'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI'
            }
        )

        self.assertEqual(401, response.status_code)


if __name__ == '__main__':
    unittest.main()
