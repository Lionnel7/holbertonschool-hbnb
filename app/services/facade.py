from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

        self.amenity_repo = InMemoryRepository()

        self.amenity_repo = InMemoryRepository()  # dépôt spécifique aux amenities

    def create_amenity(self, amenity_data):
        # Création d'une instance d'amenity avec les données reçues
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Recherche par ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Récupération de toutes les amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)


    # Users
    def create_user(self, user_data):
        """Create and store a new user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update user details if the user exists."""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        required_fields = {'first_name', 'last_name', 'email'}
        if not required_fields.issubset(user_data):
            raise TypeError('Missing required fields in payload')
        
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.user_repo.update(user_id, user_data)
        return user
    # Users

    # Places
    def create_place(self, place_data):
 
        """Create and store a new place."""

        place_data['owner'] = self.get_user(place_data.pop("owner_id"))
        place_data["amenities"] = [self.get_amenity(amenity) for amenity in place_data["amenities"]]

        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
 
        """Update place details if the place exists."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        for key in ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id', 'amenities']:
            if key in place_data:
                setattr(place, key, place_data[key])
        
        self.place_repo.update(place_id, place_data)
        return place
    # Places

    # Amenities
    def create_amenity(self, amenity_data):
        """Create and store a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)
    
    def get_amenity_by_name(self, amenity_name):
        """Retrieve an amenity by name."""
        return self.amenity_repo.get_by_attribute('name', amenity_name)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity details if the amenity exists."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity
    # Amenities

    # Reviews
    def create_review(self, review_data):
        """Create and store a new review."""

        return self.place_repo.update(place_id, place_data)

    def create_review(self, review_data):
        # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        review_data['user'] = self.get_user(review_data.pop("user_id"))
        review_data['place'] = self.get_place(review_data.pop("place_id"))
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
 
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews associated with a specific place."""
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Update review details if the review exists."""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        
        for key in ['rating', 'text', 'user_id', 'place_id']:
            if key in review_data:
                setattr(review, key, review_data[key])
        
        self.review_repo.update(review_id, review_data)
        return review
    # Reviews

        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        place = self.get_place(place_id)
        if place:
            return place.reviews    
        return None

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        self.review_repo.delete(review_id)

