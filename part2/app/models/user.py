from .base_model import BaseModel
from datetime import datetime
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = (first_name)
        self.last_name = (last_name)
        self.email = (email)
        self.is_admin = is_admin

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)):
            self._email = email
            self.save()
        else:
            raise ValueError ("Email is not conforme to standar")
    
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if(len(first_name) > 50):
            raise ValueError ("First name to long")
        else:
            self._first_name = first_name
            self.save()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if(len(last_name) > 50):
            raise ValueError ("Last name to long")
        else:
            self._last_name = last_name
            self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
