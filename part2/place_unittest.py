from app import create_app
import unittest

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    #------------- all test related to the POST request for place -------------
    def test_post_place(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        user = response.get_json()
        # ----- negative price  -----
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": -100.0, # negative value 
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        # ----- latitude between 90.0 and -90.0 -----
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 837.7749, # not between 90.0 and -90.0
            "longitude": -122.4194,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        # ----- longitude between 180.0 and -180.0 -----
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -192.4194, # not between 180.0 and -180.0
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        # ----- title to long -----
        response = self.client.post('/api/v1/places/', json={
            "title": """Cozy Apartmentddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            ffffffffffffffffffffffffffffffffffffffffffffff""", # title to long
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": 12.4194, 
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        # ----- wrong id user -----
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": 12.4194, 
            "owner_id": "fiehi", # wrong id user
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        # ----- all good -----
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": 12.4194, 
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)
        

    #------------- all test related to the GET request for place -------------
    def test_get_place(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "nath",
            "last_name": "hehe",
            "email": "nath.hehe@example.com"
        })
        user = response.get_json()
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": 12.4194, 
            "owner_id": user["id"],
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
            "first_name": "toto",
            "last_name": "Vador",
            "email": "toto.Vador@example.com"
        })
        user = response.get_json()
        response = self.client.post('/api/v1/places/', json={
            "title": "house",
            "description": "good house",
            "price": 1.0,
            "latitude": 3.7749,
            "longitude": 1.4194, 
            "owner_id": user["id"],
            "amenities": []
        })
        place = response.get_json()
        # ----- modify with good condition -----
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), json={
            "title": "toto house",
            "description": "passablegood house",
            "price": 15.0,
            "latitude": 5.7749,
            "longitude": 10.4194, 
        })
        self.assertEqual(response.status_code, 200)
        # ----- wrong place id -----
        response = self.client.put('/api/v1/places/hihi', json={
            "title": "toto house",
            "description": "passablegood house"
        })
        self.assertEqual(response.status_code, 404)
        # ----- title to long -----
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), json={
            "title": """toto houseddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            dddddddddddddddddddddddddddddddddddd""",
            "description": "passablegood house"
        })
        self.assertEqual(response.status_code, 400)
        # ----- price is negative -----
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), json={
            "price": -5,
            "description": "passablegood house"
        })
        self.assertEqual(response.status_code, 400)
        # ----- longitude is not between 180.0 and -180.0 -----
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), json={
            "longitude": -555.5,
            "description": "passablegood house"
        })
        self.assertEqual(response.status_code, 400)
        # ----- longitude is not between 90.0 and -90.0 -----
        response = self.client.put('/api/v1/places/{}'.format(place["id"]), json={
            "latitude": -555.5,
            "description": "passablegood house"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()