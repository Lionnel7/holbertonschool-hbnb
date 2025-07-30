# config.py
import os

class Config:
    """
    Classe de configuration de base pour l'application Flask.
    Contient les paramètres communs à tous les environnements.
    """
    # Clé secrète de Flask : très importante pour la sécurité (sessions, etc.)
    # Changez 'votre_super_cle_secrete_ici_svp_changez_en_production' en une chaîne aléatoire forte en production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_super_cle_secrete_ici_svp_changez_en_production'

    # Configuration de SQLAlchemy (base de données)
    # C'est ici que nous définissons le chemin et le nom par défaut de la base de données
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_test.db' # <--- C'EST LA LIGNE CLÉ MANQUANTE OU MAL PLACÉE
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Supprime un avertissement de Flask-SQLAlchemy

    # Configuration de Flask-JWT-Extended (pour les tokens d'authentification)
    # Changez 'une_autre_cle_secrete_jwt_pour_la_securite' en une chaîne aléatoire forte en production
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'une_autre_cle_secrete_jwt_pour_la_securite'
    JWT_TOKEN_LOCATION = ['headers'] # Indique où chercher les tokens JWT (par défaut, dans l'en-tête Authorization)


class DevelopmentConfig(Config):
    """
    Configuration spécifique à l'environnement de développement.
    Hérite des paramètres de Config et les surcharge si nécessaire.
    """
    DEBUG = True # Active le mode débogage pour un développement plus facile
    # Nous allons utiliser la base de données définie dans la classe Config de base.
    # Si vous vouliez une base de données *différente* pour le dev (ex: hbnb_dev.db),
    # vous décommenteriez et modifieriez la ligne ci-dessous :
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_dev.db'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """
    Configuration spécifique à l'environnement de test.
    """
    TESTING = True # Active le mode test
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Base de données en mémoire pour les tests (effacée après chaque exécution)
    JWT_SECRET_KEY = 'test_jwt_secret' # Clé JWT spécifique pour les tests


class ProductionConfig(Config):
    """
    Configuration spécifique à l'environnement de production.
    Idéalement, utilisez des variables d'environnement pour les informations sensibles ici.
    """
    # Ici, vous pourriez surcharger pour une base de données de production réelle (ex: PostgreSQL)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@host:port/dbname'
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY_PROD')
    pass
