from .base_model import BaseModel
from datetime import datetime
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner, amenities):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = amenities

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        if (isinstance(owner, User)):
            self._owner = owner
            self.save()
        else:
            raise ValueError ("owner not found")

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if(len(title) < 101):
            self._title = title
            self.save()
        else:
            raise ValueError ("Title is not conforme to standar")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if(price >= 0):
            self._price = price
            self.save()
        else:
            raise ValueError ("price must be positif")
    
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        if(latitude >= -90 and latitude <= 90):
            self._latitude = latitude
            self.save()
        else:
            raise ValueError ("latitude must be within the range of -90.0 to 90.0")

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        if(longitude >= -180 and longitude <= 180):
            self._longitude = longitude
            self.save()
        else:
            raise ValueError ("longitude must be within the range of -180.0 to 180.0")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.to_dict(),
            "amenities": [element.to_dict() for element in self.amenities]
        }
