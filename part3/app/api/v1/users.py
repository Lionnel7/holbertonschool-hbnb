from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('admin', description='Admin operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='password of the user')
})

@api.route('/')
class AdminUserCreate(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    #@jwt_required()
    def post(self):
        """Register a new user"""
        #current_user = get_jwt_identity()
        user_data = api.payload
        #if not current_user.get('is_admin'):
        #   return {'error': 'Admin privileges required'}, 403
        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            return  {'error': str(e)}, 400
        
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'No user found')
    def get(self):
        list_all = []
        user = facade.get_all_user()
        for element in user:
            list_all.append(element.to_dict())
        return list_all, 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
    
    @api.response(200, 'User details change successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Get user details by ID"""
        new_data = api.payload
        user = facade.get_user(user_id)
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        if not user:
            return {'error': 'User not found'}, 404
        elif not is_admin and user_id != current_user["id"]:
            return {'error': 'Unauthorized action.'}, 403
        if new_data.get('email'):
            existing_user = facade.get_user_by_email(new_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400
        try:
            facade.update_user(user_id=user_id, data=new_data)
            return user.to_dict(), 200
        except ValueError as e:
            return  {'error': str(e)}, 400
