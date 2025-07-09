# app/models/city.py
from app import db  # Importez l'instance de db
from .base_model import BaseModel # Importez votre BaseModel

class City(BaseModel):
    __tablename__ = 'cities'

    name = db.Column(db.String(128), nullable=False)
    # Si vous avez des relations avec d'autres modèles comme State ou Country, ajoutez-les ici
    # state_id = db.Column(db.String(60), db.ForeignKey('states.id'), nullable=False)

    # Relation avec Place (si vous voulez accéder aux places d'une ville)
    # places = db.relationship('Place', backref='city', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<City {self.name} (ID: {self.id})>"
