# app/models/base_model.py
import uuid
from datetime import datetime
from app import db # <--- IMPORTER L'INSTANCE DE DB DE FLASK-SQLALCHEMY

class BaseModel(db.Model): # <--- HÉRITER DE db.Model ICI
    __abstract__ = True # Indique à SQLAlchemy que c'est une classe abstraite, pas une table en soi

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        # Le __init__ de BaseModel est simplifié car SQLAlchemy le gère
        pass # Laissez SQLAlchemy gérer l'initialisation des colonnes

    def to_dict(self):
        # Méthode pour convertir l'objet en dictionnaire, utile pour les API
        data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # Convertir datetime en string pour la sérialisation JSON
            if isinstance(value, datetime):
                data[column.name] = value.isoformat()
            else:
                data[column.name] = value
        return data

    def save(self):
        # Méthode pour ajouter et committer l'objet à la session de DB
        db.session.add(self)
        db.session.commit()

    def delete(self):
        # Méthode pour supprimer l'objet de la session de DB
        db.session.delete(self)
        db.session.commit()
