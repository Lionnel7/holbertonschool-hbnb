# app/__init__.py

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import os


# Initialisation des extensions Flask
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Crée et configure l'application Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions avec l'application Flask
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Configuration de l'API Flask-RESTx
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/', # Rend la documentation Swagger accessible à la racine /
    )

    # Importation et ajout des Namespaces (vos modules d'API)
    # Assurez-vous que ces imports sont corrects par rapport à votre structure de fichiers
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns # <-- Modifié/Ajouté pour Place
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.admin import api as admin_ns # <-- Ajouté pour Admin

    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places') # <-- Ajouté pour Place
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin') # <-- Ajouté pour Admin


    # --- DÉBUT DE LA SECTION CRUCIALE POUR LA CRÉATION DES TABLES ---
    # Importez TOUS vos modèles ici pour que SQLAlchemy puisse les "voir"
    # et créer les tables correspondantes dans la base de données.
    from app.models.user import User
    from app.models.amenity import Amenity
    from app.models.city import City
    from app.models.place import Place
    from app.models.review import Review

    # Créez les tables de la base de données DANS le contexte de l'application.
    with app.app_context():
        print("DEBUG: TENTATIVE DE CRÉATION DES TABLES...")
        try:
            db.create_all()
            print("DEBUG: db.create_all() EXÉCUTÉ SANS ERREUR.")

            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables_in_db = inspector.get_table_names()
            print(f"DEBUG: Tables trouvées par SQLAlchemy APRES création: {tables_in_db}")

        except Exception as e:
            print(f"ERREUR LORS DE db.create_all(): {e}")
            import traceback
            traceback.print_exc()

        print("DEBUG: FIN DU BLOC DE CRÉATION DES TABLES.")
    # --- FIN DE LA SECTION CRUCIALE POUR LA CRÉATION DES TABLES ---

    return app
