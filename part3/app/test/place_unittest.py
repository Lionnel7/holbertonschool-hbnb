from app import create_app
import unittest

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    #===============================================================
    # ----- test all request basic work and value error -----
    #===============================================================
    def test_post_place(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        user = response.get_json()
        # ----- negative price  -----
        response = self.client.post('/api/v1/places/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": -100.0, # negative value 
            "latitude": 37.7749,
            "longitude": -122.4194,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        # ----- latitude between 90.0 and -90.0 -----
        response = self.client.post('/api/v1/places/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 837.7749, # not between 90.0 and -90.0
            "longitude": -122.4194,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        # ----- longitude between 180.0 and -180.0 -----
        response = self.client.post('/api/v1/places/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -192.4194, # not between 180.0 and -180.0
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        # ----- title to long -----
        response = self.client.post('/api/v1/places/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": """Cozy Apartmentddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ffffffffffffffffffffffffffffffffffffffffffffff""", # title to long
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": 12.4194, 
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        # ----- all good -----
        response = self.client.post('/api/v1/places/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": 12.4194, 
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)
        

    #------------- all test related to the GET request for place -------------
    def test_get_place(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        user = response.get_json()
        response = self.client.post('/api/v1/places/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": 12.4194, 
            "amenities": []
        })
        place = response.get_json()
        # ----- get all -----
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        # ----- get one -----
        response = self.client.get('/api/v1/places/{}'.format(place["id"]))
        self.assertEqual(response.status_code, 200)
        # ----- get unknow -----
        response = self.client.get('/api/v1/places/Hugohouse')
        self.assertEqual(response.status_code, 404)
    
    #------------- all test related to modify place data -------------
    def test_put_place(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        user = response.get_json()
        response = self.client.post('/api/v1/places/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "house",
            "description": "good house",
            "price": 1.0,
            "latitude": 3.7749,
            "longitude": 1.4194, 
            "amenities": []
        })
        place = response.get_json()
        # ----- modify with good condition -----
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "toto house",
            "description": "passablegood house",
            "price": 15.0,
            "latitude": 5.7749,
            "longitude": 10.4194, 
        })
        self.assertEqual(response.status_code, 200)
        # ----- wrong place id -----
        response = self.client.put('/api/v1/places/hihi', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "toto house",
            "description": "passablegood house"
        })
        self.assertEqual(response.status_code, 404)
        # ----- title to long -----
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": """toto houseddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            dddddddddddddddddddddddddddddddddddd""",
            "description": "passablegood house"
        })
        self.assertEqual(response.status_code, 400)
        # ----- price is negative -----
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "price": -5,
            "description": "passablegood house"
        })
        self.assertEqual(response.status_code, 400)
        # ----- longitude is not between 180.0 and -180.0 -----
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "longitude": -555.5,
            "description": "passablegood house"
        })
        self.assertEqual(response.status_code, 400)
        # ----- longitude is not between 90.0 and -90.0 -----
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "latitude": -555.5,
            "description": "passablegood house"
        })
        self.assertEqual(response.status_code, 400)

    #===============================================================
    # ----- test all JWT access for all route that use it -----
    #===============================================================
    def test_put_place(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "nath",
            "last_name": "Dup",
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        # test all route with jwt protection with login 
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.post('/api/v1/places/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "amenities": []
        })
        place = response.get_json()
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "latitude": -55.5,
            "description": "passable good house"
        })
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "latitude": 33.5,
            "description": "g éme po"
        })
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()