# app/models/user.py

from app import db, bcrypt
from app.models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    # C'est la modification cruciale !
    def __init__(self, **kwargs):
        # Passer tous les arguments nommés à la méthode __init__ de la classe parente (db.Model via BaseModel)
        # SQLAlchemy utilisera ces kwargs pour initialiser les attributs correspondants aux colonnes.
        super().__init__(**kwargs) 
        
        # Le setter de mot de passe est un cas spécial.
        # Il prend 'password' et l'hache pour stocker dans 'password_hash'.
        # Nous l'appelons ici pour s'assurer que le hachage se produit au moment de la création.
        if 'password' in kwargs:
            self.password = kwargs['password'] 

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
