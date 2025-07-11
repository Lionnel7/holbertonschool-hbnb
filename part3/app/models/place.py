import uuid
from datetime import datetime
from app.models.__init__ import BaseModel, db

place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):

    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    _title = db.Column(db.String(50), nullable=False)
    _description = db.Column(db.String(50), nullable=False)
    _price = db.Column(db.String(120), nullable=False, unique=True)
    latitude = db.Column(db.Float, default=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                              backref=db.backref('places', lazy=True))

    def __init__(self, title='', description='', price='', latitude=0.0, longitude=0.0, owner_id=''):
        self.id = str(uuid.uuid4())
        self._title = title
        self._description = description
        self._price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if len(value) > 100:
            raise TypeError("Error: title is invalid")
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price can't be negative")
        self._price = value

    def set_coordinates(self, latitude, longitude):
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            raise ValueError("Coordinates of latitude and longitude aren't correct")
        self._latitude = latitude
        self._longitude = longitude

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def add_user(self, user):
        """Add a user to the place"""
        self.users.append(user)
