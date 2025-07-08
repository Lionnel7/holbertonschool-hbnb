#!/usr/bin/python3
from datetime import datetime
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    def __init__(self, place, user, rating, text):
        """Initialize a new Review instance."""
        super().__init__()
        self.place = place
        self.user = user
        self.rating = rating
        self.text = text

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, place):
        if isinstance(place, Place):
            self._place = place.id
            self.save()
        else:
            raise ValueError ("Place do not exist")

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if isinstance(user, User):
            self._user = user.id
            self.save()
        else:
            raise ValueError ("User do not exist")

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        if (rating > 0 and rating < 6):       
            self._rating = rating
            self.save()
        else:
            raise ValueError ("rating must be between 1 and 5")

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if (len(text) > 0):       
            self._text = text
            self.save()
        else:
            raise ValueError ("the text must not be empty")

    def to_dict(self):
        return {
            'id': self.id,
            'place': self.place,
            'user': self.user,
            'rating': self.rating,
            'text': self.text
        }
