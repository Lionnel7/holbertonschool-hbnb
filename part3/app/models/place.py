# app/models/place.py
from app import db # Importez l'instance de db
from .base_model import BaseModel # Importez votre BaseModel
# Si vous avez besoin d'importer d'autres modèles pour les relations (ex: User, Amenity)
# from app.models.user import User
# from app.models.amenity import Amenity

# Définition de la table d'association pour la relation Many-to-Many Place <-> Amenity
# Cette table doit être définie ici ou dans un fichier d'associations séparé
# car elle n'a pas de classe de modèle propre.
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(60), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    # Clé étrangère pour la relation Many-to-One avec User (l'hôte)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    number_rooms = db.Column(db.Integer, default=0, nullable=False)
    number_bathrooms = db.Column(db.Integer, default=0, nullable=False)
    max_guest = db.Column(db.Integer, default=0, nullable=False)
    price_by_night = db.Column(db.Integer, default=0, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    city_id = db.Column(db.String(60), db.ForeignKey('cities.id'), nullable=False) # Assurez-vous d'avoir un modèle City si vous l'utilisez

    # Relations (si vous les définissez ici)
    # reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")
    # amenities = db.relationship(
    #     'Amenity', secondary=place_amenity,
    #     backref=db.backref('places', lazy=True),
    #     lazy='dynamic' # lazy='dynamic' pour permettre le filtrage sur la relation
    # )

    def __repr__(self):
        return f"<Place {self.name} (ID: {self.id})>"

    # Supprimez la méthode __init__ si elle ne fait que des attributions de base
    # Laissez SQLAlchemy gérer la création des objets à partir des arguments-clés.
    # Ex: place = Place(name="Maison", description="Belle maison")
