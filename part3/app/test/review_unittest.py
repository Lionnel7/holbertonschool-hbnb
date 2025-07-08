from app import create_app
import unittest

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    #===============================================================
    # ----- test all request basic work and value error -----
    #===============================================================
    def test_post_review(self):
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
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "text": "Great place to stay!",
            "rating": 6,
            "place_id": place["id"]
        })
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": "totohouse"
        })
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": place["id"]
        })
        self.assertEqual(response.status_code, 201)

    #------------- all test related to the GET request for review -------------
    def test_get_review(self):
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
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": place["id"]
        })
        review = response.get_json()["id"]
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/reviews/{}'.format(review))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/reviews/toto')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/api/v1/reviews/places/toto/reviews')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/api/v1/reviews/places/{}/reviews'.format(place["id"]))
        self.assertEqual(response.status_code, 200)
        
    #------------- all test related to the PUT request for review -------------
    def test_put_review(self):
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
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)},json={
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": place["id"]
        })
        review = response.get_json()
        response = self.client.put('/api/v1/reviews/toto', headers={'Authorization': 'Bearer {}'.format(current_tok)},json={
            "text": "Great place to stay!",
            "rating": 5,
        })
        self.assertEqual(response.status_code, 404)
        response = self.client.put('/api/v1/reviews/{}'.format(review["id"]), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "ugly",
            "rating": -45
        })
        self.assertEqual(response.status_code, 400)
        response = self.client.put('/api/v1/reviews/{}'.format(review["id"]), headers={'Authorization': 'Bearer {}'.format(current_tok)}, json={
            "title": "ugly",
            "rating": 1
        })
        self.assertEqual(response.status_code, 200)

    #------------- all test related to the DELETE request for review -------------
    def test_delete_review(self):
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
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)},json={
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": place["id"]
        })
        review = response.get_json()
        response = self.client.delete('/api/v1/reviews/hihi', headers={'Authorization': 'Bearer {}'.format(current_tok)})
        self.assertEqual(response.status_code, 404)
        response = self.client.delete('/api/v1/reviews/{}'.format(review["id"]), headers={'Authorization': 'Bearer {}'.format(current_tok)})
        self.assertEqual(response.status_code, 200)

    #===============================================================
    # ----- test JWT access for all route that use it -----
    #===============================================================
    def test_JWT_post_review(self):
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
        # try to review the place as the creator of it
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)},json={
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": place["id"]
        })
        self.assertEqual(response.status_code, 400)
        # try to review the place as a normal user for the first time
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)},json={
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": place["id"]
        })
        self.assertEqual(response.status_code, 201)
        # try to review a second time the same place
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)},json={
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": place["id"]
        })
        self.assertEqual(response.status_code, 400) 

    def test_JWT_put_review(self):
        # create the users the place and the review
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
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)},json={
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": place["id"]
        })
        review_test = response.get_json()
        # try to modify the review as another user
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.put('/api/v1/reviews/{}'.format(review_test['id']), headers={'Authorization': 'Bearer {}'.format(current_tok)},json={
            "text": "worst place to stay!",
            "rating": 1
        })
        self.assertEqual(response.status_code, 403)
        # try to modify the review as the writer
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.put('/api/v1/reviews/{}'.format(review_test['id']), headers={'Authorization': 'Bearer {}'.format(current_tok)},json={
            "text": "worst place to stay!",
            "rating": 1
        })
        
        self.assertEqual(response.status_code, 200) 

    def test_JWT_delete_review(self):
        # create the users the place and the review
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
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.post('/api/v1/reviews/', headers={'Authorization': 'Bearer {}'.format(current_tok)},json={
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": place["id"]
        })
        review_test = response.get_json()
        # try to delete the review as another user
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane.doe@example.com",
            "password": "toto"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.delete('/api/v1/reviews/{}'.format(review_test['id']), headers={'Authorization': 'Bearer {}'.format(current_tok)})
        self.assertEqual(response.status_code, 403)
        # try to delete the review as the writer
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nat.dup@example.com",
            "password": "toto1"
        })
        current_tok = response.get_json()["access_token"]
        response = self.client.delete('/api/v1/reviews/{}'.format(review_test['id']), headers={'Authorization': 'Bearer {}'.format(current_tok)})
        
        self.assertEqual(response.status_code, 200) 

if __name__ == '__main__':
    unittest.main()