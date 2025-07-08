from app import create_app
import unittest

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    #------------- all test related to the POST request for review -------------
    def test_post_place(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
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
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user["id"],
            "place_id": place["id"]
        })
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 6,
            "user_id": user["id"],
            "place_id": place["id"]
        })
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "toto",
            "place_id": place["id"]
        })
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user["id"],
            "place_id": "totohouse"
        })
        self.assertEqual(response.status_code, 400)

    #------------- all test related to the GET request for review -------------
    def test_get_place(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane1",
            "last_name": "Doe1",
            "email": "jane1.doe@example.com"
        })
        user = response.get_json()
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment1",
            "description": "A nice place to stay1",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": 12.4194, 
            "owner_id": user["id"],
            "amenities": []
        })
        place = response.get_json()
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user["id"],
            "place_id": place["id"]
        })
        review = response.get_json()
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/reviews/{}'.format(review["id"]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/reviews/toto')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/api/v1/reviews/places/toto/reviews')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/api/v1/reviews/places/{}/reviews'.format(place["id"]))
        self.assertEqual(response.status_code, 200)
        
    #------------- all test related to the GET request for review -------------
    def test_put_place(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane2",
            "last_name": "Doe2",
            "email": "jane.doe2@example.com"
        })
        user = response.get_json()
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment2",
            "description": "A nice place to stay2",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": 12.4194, 
            "owner_id": user["id"],
            "amenities": []
        })
        place = response.get_json()
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user["id"],
            "place_id": place["id"]
        })
        review = response.get_json()
        response = self.client.put('/api/v1/reviews/hihi', json={
            "title": "ugly",
            "rating": 1
        })
        self.assertEqual(response.status_code, 404)
        response = self.client.put('/api/v1/reviews/{}'.format(review["id"]), json={
            "title": "ugly",
            "rating": 45
        })
        self.assertEqual(response.status_code, 400)

    #------------- all test related to the DELETE request for review -------------
    def test_delete_place(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane3",
            "last_name": "Doe3",
            "email": "jane.doe3@example.com"
        })
        user = response.get_json()
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment2",
            "description": "A nice place to stay2",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": 12.4194, 
            "owner_id": user["id"],
            "amenities": []
        })
        place = response.get_json()
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user["id"],
            "place_id": place["id"]
        })
        review = response.get_json()
        response = self.client.delete('/api/v1/reviews/hihi')
        self.assertEqual(response.status_code, 404)
        response = self.client.delete('/api/v1/reviews/{}'.format(review["id"]))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()