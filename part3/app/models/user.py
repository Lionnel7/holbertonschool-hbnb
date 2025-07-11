import uuid
from datetime import datetime
from .__init__ import BaseModel, db, bcrypt


class User(BaseModel):

    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __init__(self, first_name='', last_name='', email='', is_admin=False, password=''):

        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.place = []
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def validation(self, first_name, last_name, is_admin):
            if len(self.first_name) > 50 or len(self.last_name) > 50:
                raise ValueError("First name or last name is too long!")
            if not isinstance(self.is_admin, bool):
                raise ValueError("Must be admin!")
            self.first_name = first_name
            self.last_name = last_name
            self.is_admin = True

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def add_place(self, place):
        """Add a review to the place."""
        self.place.append(place)
        
    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
