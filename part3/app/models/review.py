# app/models/review.py
from app import db # Importez l'instance de db
from .base_model import BaseModel # Importez votre BaseModel
# from app.models.user import User # Si vous avez besoin de User pour la relation
# from app.models.place import Place # Si vous avez besoin de Place pour la relation

class Review(BaseModel):
    __tablename__ = 'reviews'

    # Clés étrangères pour les relations Many-to-One
    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    text = db.Column(db.String(1024), nullable=False) # Contenu de la critique
    rating = db.Column(db.Integer, nullable=False) # Note de la critique (ex: de 1 à 5)

    def __repr__(self):
        return f"<Review {self.id} for Place {self.place_id} by User {self.user_id}>"

    # Supprimez la méthode __init__ si elle ne fait que des attributions de base
