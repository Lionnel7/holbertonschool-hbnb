from .base_model import BaseModel
from datetime import datetime

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if(len(name) <= 50):
            self._name = name
            self.save()
        else:
            raise ValueError ("name is too long")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }