# app/api/v1/users.py

from flask_restx import Namespace, Resource, fields, abort
from flask import request # Importez request au cas où vous en auriez besoin pour d'autres debugs, ou pour des requêtes complexes
from app.models.user import User
from app import db, bcrypt # Assurez-vous que db et bcrypt sont bien importés depuis app/__init__.py

print("DEBUG: Fichier users.py CHARGÉ ET EXÉCUTÉ !!!") # <--- PREMIER POINT DE DEBUG - POUR VÉRIFIER LE CHARGEMENT DU FICHIER

api = Namespace('users', description='Opérations liées aux utilisateurs')

# Modèle de sortie pour un utilisateur (ce que l'API renvoie)
user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='Identifiant unique de l\'utilisateur'),
    'email': fields.String(required=True, description='Adresse email de l\'utilisateur'),
    'first_name': fields.String(required=True, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=True, description='Nom de l\'utilisateur'),
    'is_admin': fields.Boolean(description='Indique si l\'utilisateur est un administrateur'),
    'created_at': fields.DateTime(readOnly=True, description='Date de création'),
    'updated_at': fields.DateTime(readOnly=True, description='Date de dernière mise à jour')
})

# Ce modèle sera utilisé pour valider l'entrée (payload) lors de la création d'un utilisateur
# Il est crucial d'inclure 'password' car il est envoyé dans le payload d'entrée
user_create_input_model = api.model('UserCreateInput', {
    'email': fields.String(required=True, description='Adresse email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur'),
    'first_name': fields.String(required=True, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=True, description='Nom de l\'utilisateur'),
    'is_admin': fields.Boolean(default=False, description='Indique si l\'utilisateur est admin (par défaut False)')
})

# Ce modèle sera utilisé pour valider l'entrée (payload) lors de la mise à jour d'un utilisateur
# Tous les champs sont optionnels pour une mise à jour
user_update_input_model = api.model('UserUpdateInput', {
    'email': fields.String(description='Adresse email de l\'utilisateur'),
    'password': fields.String(description='Nouveau mot de passe de l\'utilisateur'),
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de l\'utilisateur'),
    'is_admin': fields.Boolean(description='Indique si l\'utilisateur est un administrateur')
})


# --- Ressource pour gérer TOUS les utilisateurs (GET all, POST) ---
@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model, code=200)
    def get(self):
        """Récupère la liste de tous les utilisateurs."""
        users = User.query.all()
        return users

    @api.doc('create_user')
    # Utilisation du modèle d'entrée spécifique pour la création (avec mot de passe)
    @api.expect(user_create_input_model, validate=True) # <-- IMPORTANT : Valide l'entrée JSON
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Crée un nouvel utilisateur."""
        data = api.payload # Récupère directement le corps JSON de la requête
        print(f"DEBUG: Données reçues par l'API (post): {data}") # <-- DEUXIÈME POINT DE DEBUG - POUR VÉRIFIER LES DONNÉES JSON

        try:
            new_user = User(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password'], # Le setter du modèle User hachera ceci
                is_admin=data.get('is_admin', False) # Utilisation de .get() pour gérer le cas où is_admin n'est pas fourni
            )
            new_user.save()

            return new_user, 201

        except ValueError as e:
            db.session.rollback() # Annule les changements en cas d'erreur de validation métier
            api.abort(400, message=str(e))
        except Exception as e:
            db.session.rollback() # Annule les changements en cas d'erreur de base de données
            # Log l'erreur interne complète pour le débogage côté serveur
            import traceback
            traceback.print_exc()
            api.abort(500, message=f"Une erreur interne est survenue: {str(e)}")


# --- Ressource pour gérer un utilisateur spécifique par son ID (GET, PUT, DELETE) ---
@api.route('/<string:user_id>')
@api.param('user_id', 'L\'identifiant unique de l\'utilisateur')
@api.response(404, 'Utilisateur non trouvé')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Récupère les informations d'un utilisateur spécifique."""
        user = User.query.get_or_404(user_id)
        return user

    @api.doc('update_user')
    @api.expect(user_update_input_model, validate=True) # Utilise le modèle d'entrée pour la mise à jour
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Met à jour un utilisateur existant."""
        user = User.query.get_or_404(user_id)
        data = api.payload
        print(f"DEBUG: Données reçues par l'API (post): {data}") # DEBUG

        try:
            if 'email' in data:
                user.email = data['email']
            if 'password' in data:
                user.password = data['password'] # Le setter du modèle User hachera ceci
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'is_admin' in data:
                user.is_admin = data['is_admin']

            user.save()

            return user

        except ValueError as e:
            db.session.rollback()
            api.abort(400, message=str(e))
        except Exception as e:
            db.session.rollback()
            import traceback
            traceback.print_exc()
            api.abort(500, message=f"Une erreur interne est survenue: {str(e)}")


    @api.doc('delete_user')
    @api.response(204, 'Utilisateur supprimé avec succès')
    def delete(self, user_id):
        """Supprime un utilisateur."""
        user = User.query.get_or_404(user_id)
        user.delete()
        return '', 204
