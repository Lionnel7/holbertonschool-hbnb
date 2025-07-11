import uuid
from datetime import datetime
from app.models.__init__ import BaseModel, db

class Review(db.Model):

    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id, id=None):
        if not text:
            raise ValueError("Review text is required")
        self.text = text

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        self.rating = rating

        if not isinstance(place_id, str):
            raise ValueError("Invalid Place ID")
        self.place_id = place_id

        if not isinstance(user_id, str):
            raise ValueError("Invalid User ID")
        self.user_id = user_id

        self.id = id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()

    def dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
