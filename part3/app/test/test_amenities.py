from app import create_app
import unittest

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    #------------- all test related to creation of amenities -------------
    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 201)
        amenity = response.get_json()
        self.assertIn("id", amenity)
        self.assertEqual(amenity["name"], "Wi-Fi")

    def test_create_amenity_empty_name(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    #------------- all test related to retrieving amenities -------------
    def test_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_amenity_by_id(self):
        # Créer une amenity pour pouvoir la récupérer ensuite
        post_response = self.client.post('/api/v1/amenities/', json={
            "name": "Pool"
        })
        self.assertEqual(post_response.status_code, 201)
        amenity = post_response.get_json()

        get_response = self.client.get(f"/api/v1/amenities/{amenity['id']}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.get_json()["name"], "Pool")

    def test_get_amenity_invalid_id(self):
        response = self.client.get("/api/v1/amenities/invalid-id-1234")
        self.assertEqual(response.status_code, 404)

    #------------- all test related to updating amenities -------------
    def test_update_amenity_success(self):
        # Create amenity
        post_response = self.client.post('/api/v1/amenities/', json={
            "name": "Gym"
        })
        amenity = post_response.get_json()

        # update
        put_response = self.client.put(f"/api/v1/amenities/{amenity['id']}", json={
            "name": "Fitness Room"
        })
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.get_json()["message"], "Amenity updated successfully")

    def test_update_amenity_invalid_id(self):
        response = self.client.put("/api/v1/amenities/invalid-id-1234", json={
            "name": "Updated Amenity"
        })
        self.assertEqual(response.status_code, 404)

    def test_update_amenity_empty_name(self):
        # Créer une amenity
        post_response = self.client.post('/api/v1/amenities/', json={
            "name": "Parking"
        })
        amenity = post_response.get_json()

        # Mise à jour avec nom vide
        put_response = self.client.put(f"/api/v1/amenities/{amenity['id']}", json={
            "name": ""
        })
        self.assertEqual(put_response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
