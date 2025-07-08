from flask_restx import Namespace, Resource, fields
from app.services import facade
import re 

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            return  {'error': str(e)}, 400

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

@api.route('/')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'No user found')
    def get(self):
        list_all = []
        user = facade.get_all_user()
        for element in user:
            list_all.append(element.to_dict())
        return list_all, 200

@api.route('/<user_id>')
class UserChange(Resource):
    @api.response(200, 'User details change successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Get user details by ID"""
        new_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        if facade.get_user_by_email(new_data['email']):
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.update_user(user_id=user_id, data=new_data)
            return user.to_dict(), 200
        except ValueError as e:
            return  {'error': str(e)}, 400
