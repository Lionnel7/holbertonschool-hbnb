# app/api/v1/admin.py

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.models.user import User # Pour les opérations sur les utilisateurs
from app import db # Importez l'instance de db (si vous l'utilisez directement)

api = Namespace('admin', description='Admin operations')

# Modèle pour la création/mise à jour d'utilisateur via l'API Admin
admin_user_model = api.model('AdminUser', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=False, description='password of the user (optional for update)'),
    'is_admin': fields.Boolean(description='Set true if user is admin') # L'admin peut définir ce champ
})

@api.route('/users') # Endpoint pour gérer les utilisateurs en tant qu'admin
class AdminUsersList(Resource):
    # @jwt_required() # Décommenter pour exiger authentification JWT
    @api.expect(admin_user_model, validate=True) # Utilise le modèle pour l'entrée
    @api.response(201, 'User successfully created by admin')
    @api.response(400, 'Invalid input data or email already registered')
    def post(self):
        """Register a new user as an admin."""
        # current_user = get_jwt_identity()
        # if not current_user.get('is_admin'):
        #     return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            api.abort(400, 'Email already registered')

        try:
            new_user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password'],
                is_admin=user_data.get('is_admin', False)
            )
            new_user.save()
            return {'message': f"User {new_user.email} created successfully by admin", 'id': new_user.id}, 201
        except ValueError as e:
            api.abort(400, message=str(e))
        except Exception as e:
            api.abort(500, message=f"Internal server error: {str(e)}")

    # @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    def get(self):
        """Get all users (admin view)."""
        # current_user = get_jwt_identity()
        # if not current_user.get('is_admin'):
        #     return {'error': 'Admin privileges required'}, 403

        users = User.query.all()
        return [user.to_dict() for user in users], 200

@api.route('/users/<string:user_id>')
class AdminUserResource(Resource):
    # @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID (admin view)."""
        # current_user = get_jwt_identity()
        # if not current_user.get('is_admin'):
        #     return {'error': 'Admin privileges required'}, 403

        user = User.query.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict(), 200

    # @jwt_required()
    @api.expect(admin_user_model, validate=False)
    @api.response(200, 'User details updated by admin successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details by ID (admin view)."""
        # current_user = get_jwt_identity()
        # if not current_user.get('is_admin'):
        #     return {'error': 'Admin privileges required'}, 403

        user = User.query.get(user_id)
        if not user:
            api.abort(404, 'User not found')

        data = api.payload
        try:
            if 'first_name' in data: user.first_name = data['first_name']
            if 'last_name' in data: user.last_name = data['last_name']
            if 'email' in data:
                existing_user = User.query.filter_by(email=data['email']).first()
                if existing_user and existing_user.id != user_id:
                    api.abort(400, 'Email already in use')
                user.email = data['email']
            if 'password' in data: user.password = data['password']
            if 'is_admin' in data: user.is_admin = data['is_admin']

            user.save()
            return user.to_dict(), 200
        except ValueError as e:
            api.abort(400, message=str(e))
        except Exception as e:
            api.abort(500, message=f"Internal server error: {str(e)}")

    # @jwt_required()
    @api.response(204, 'User deleted by admin successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete user by ID (admin view)."""
        # current_user = get_jwt_identity()
        # if not current_user.get('is_admin'):
        #     return {'error': 'Admin privileges required'}, 403

        user = User.query.get(user_id)
        if not user:
            api.abort(404, 'User not found')

        user.delete()
        return '', 204
