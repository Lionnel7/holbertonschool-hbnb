import requests
import pytest 


class TestUsers:
    def test_create_user_success(self):
        """Test de création d'un utilisateur avec succès"""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": generate_unique_email(), # Utilisé via conftest ou importé
            "password": "SecurePassword123!"
        }
        response = requests.post(f"{BASE_URL}/users/", json=user_data)

        assert response.status_code == 201, f"Response: {response.text}"

        user = response.json()
        assert "id" in user
        assert user["first_name"] == user_data["first_name"]
        assert user["last_name"] == user_data["last_name"]
        assert user["email"] == user_data["email"]
        assert "password" not in user

    def test_create_user_missing_fields(self):
        """Test de création d'un utilisateur avec des champs manquants"""
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe"
        }
        response = requests.post(f"{BASE_URL}/users/", json=user_data)

        assert response.status_code == 400, f"Response: {response.text}"

        data = response.json()
        assert "error" in data

    def test_create_user_duplicate_email(self):
        """Test de création d'un utilisateur avec un email déjà utilisé"""
        email = generate_unique_email()

        user_data1 = {
            "first_name": "Original",
            "last_name": "User",
            "email": email,
            "password": "Password123!"
        }
        response1 = requests.post(f"{BASE_URL}/users/", json=user_data1)
        assert response1.status_code == 201, f"Failed to create first user: {response1.text}"

        user_data2 = {
            "first_name": "Duplicate",
            "last_name": "User",
            "email": email,
            "password": "Password456!"
        }
        response2 = requests.post(f"{BASE_URL}/users/", json=user_data2)

        assert response2.status_code == 400, f"Response: {response2.text}"

        data = response2.json()
        assert "error" in data

    def test_get_all_users(self):
        """Test pour récupérer tous les utilisateurs"""
        response = requests.get(f"{BASE_URL}/users/")

        assert response.status_code == 200, f"Response: {response.text}"

        data = response.json()
        assert "users" in data
        assert isinstance(data["users"], list)

    def test_get_user_by_id(self, create_test_user):
        """Test pour récupérer un utilisateur par son ID"""
        user_id = create_test_user["id"]
        response = requests.get(f"{BASE_URL}/users/{user_id}")

        assert response.status_code == 200, f"Response: {response.text}"

        user = response.json()
        assert user["id"] == user_id
        assert user["first_name"] == create_test_user["first_name"]
        assert user["last_name"] == create_test_user["last_name"]
        assert user["email"] == create_test_user["email"]

    def test_get_user_not_found(self):
        """Test pour récupérer un utilisateur qui n'existe pas"""
        nonexistent_id = str(uuid.uuid4())
        response = requests.get(f"{BASE_URL}/users/{nonexistent_id}")

        assert response.status_code == 404, f"Response: {response.text}"

        data = response.json()
        assert "error" in data

    def test_update_user(self, create_test_user):
        """Test pour mettre à jour un utilisateur"""
        user_id = create_test_user["id"]
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": generate_unique_email(),
            "password": "NewPassword123!"
        }
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)

        assert response.status_code == 200, f"Response: {response.text}"

        updated_user = response.json()
        assert updated_user["id"] == user_id
        assert updated_user["first_name"] == update_data["first_name"]
        assert updated_user["last_name"] == update_data["last_name"]
        assert updated_user["email"] == update_data["email"]
