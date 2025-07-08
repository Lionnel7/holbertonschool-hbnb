from app import create_app
import unittest

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    #------------- all test related at the creation of the user -------------
    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_first_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": """dddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddd""",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_last_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": """dddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddd""",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

    #------------- all test related to get the user data -------------
    def test_get_user_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane1",
            "last_name": "Doe1",
            "email": "jane1.doe@example.com"
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
            "first_name": "Jane2",
            "last_name": "Doe2",
            "email": "jane2.doe@example.com"
        })
        user = response.get_json()
        response = self.client.put('/api/v1/users/{}'.format(user['id']), json={
            "first_name": "tata",
            "last_name": "Mia",
            "email": "tata.Mia@example.com"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane3",
            "last_name": "Doe3",
            "email": "jane3.doe@example.com"
        })
        user = response.get_json()
        response = self.client.put('/api/v1/users/{}'.format(user['id']), json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_invalid_first_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane4",
            "last_name": "Doe4",
            "email": "jane4.doe@example.com"
        })
        user = response.get_json()
        response = self.client.put('/api/v1/users/{}'.format(user['id']), json={
            "first_name": """dddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddd""",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_invalid_last_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane5",
            "last_name": "Doe5",
            "email": "jane5.doe@example.com"
        })
        user = response.get_json()
        response = self.client.put('/api/v1/users/{}'.format(user['id']), json={
            "first_name": "Jane",
            "last_name": """dddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddd""",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_wrong_user(self):
        response = self.client.put('/api/v1/users/1234abec', json={
            "first_name": "Jane6",
            "last_name": "Doe6",
            "email": "jane6.doe@example.com"
        })
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()