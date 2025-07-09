# app/models/amenity.py
from app import db # Importez l'instance de db
from .base_model import BaseModel # Importez votre BaseModel
# from app.models.place import place_amenity # Si la table d'association est définie ailleurs

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(128), nullable=False, unique=True) # Nom de l'équipement

    # Relation Many-to-Many avec Place (définie sur le modèle Place)
    # Si vous voulez un accès depuis Amenity vers Place, la backref 'places' est définie sur Place.amenities

    def __repr__(self):
        return f"<Amenity {self.name} (ID: {self.id})>"

    # Supprimez la méthode __init__ si elle ne fait que des attributions de base
