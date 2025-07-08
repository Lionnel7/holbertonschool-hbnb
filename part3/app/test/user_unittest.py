from app import create_app
import unittest

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    #===============================================================
    # ----- test all request basic work and value error -----
    #===============================================================
    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "password": "toto"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_first_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": """dddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddd""",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_last_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": """dddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddd""",
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        self.assertEqual(response.status_code, 400)

    #------------- all test related to get the user data -------------
    def test_get_user_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane1",
            "last_name": "Doe1",
            "email": "jane1.doe@example.com",
            "password": "toto"
        })
        user = response.get_json()
        response = self.client.get('/api/v1/users/{}'.format(user["id"]))
        self.assertEqual(response.status_code, 200)

    def test_get_wrong_user(self):
        response = self.client.get('/api/v1/users/{}'.format("1234abec"))
        self.assertEqual(response.status_code, 404)

    #------------- all test related to get all user data -------------
    def test_get_all_user(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
    
    #------------- all test related to modify user data -------------
    def test_update_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane7",
            "last_name": "Doe7",
            "email": "jane7.doe@example.com",
            "password": "toto"
        })
        user = response.get_json()
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane7.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.put('/api/v1/users/{}'.format(user['id']), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "first_name": "tata",
            "last_name": "Mia",
        })
        self.assertEqual(response.status_code, 200)

    def test_update_user_empty_first_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe3",
            "email": "jane3.doe@example.com",
            "password": "toto"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_empty_last_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane3",
            "last_name": "",
            "email": "jane3.doe@example.com",
            "password": "toto"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_invalid_first_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane4",
            "last_name": "Doe4",
            "email": "jane4.doe@example.com",
            "password": "toto"
        })
        user = response.get_json()
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane4.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.put('/api/v1/users/{}'.format(user['id']), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "first_name": """dddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddd""",
            "last_name": "Doe",
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_invalid_last_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane5",
            "last_name": "Doe5",
            "email": "jane5.doe@example.com",
            "password": "toto"
        })
        user = response.get_json()
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane5.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.put('/api/v1/users/{}'.format(user['id']), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "first_name": "Jane",
            "last_name": """dddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddd""",
        })
        self.assertEqual(response.status_code, 400)

    def test_update_wrong_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane8",
            "last_name": "Doe8",
            "email": "jane8.doe@example.com",
            "password": "toto"
        })
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane8.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.put('/api/v1/users/1234abec', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "first_name": "Jane8.1",
            "last_name": "Doe8.1",
        })
        self.assertEqual(response.status_code, 404)

    #===============================================================
    # ----- test JWT access for all route that use it -----
    #===============================================================

    def test_JWT_put_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane9",
            "last_name": "Doe9",
            "email": "jane9.doe@example.com",
            "password": "toto"
        })
        user = response.get_json()
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane10",
            "last_name": "Doe10",
            "email": "jane10.doe@example.com",
            "password": "toto"
        })
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane10.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.put('/api/v1/users/{}'.format(user['id']), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "first_name": "Jane9.1",
            "last_name": "Doe9.1"
        })
        self.assertEqual(response.status_code, 403)
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane9.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.put('/api/v1/users/{}'.format(user['id']), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "first_name": "Jane9.1",
            "last_name": "Doe9.1",
            "email": "toto@changement.com"
        })
        self.assertEqual(response.status_code, 400)
        response = self.client.put('/api/v1/users/{}'.format(user['id']), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "first_name": "Jane9.1",
            "last_name": "Doe9.1",
            "password": "saucetomate"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()