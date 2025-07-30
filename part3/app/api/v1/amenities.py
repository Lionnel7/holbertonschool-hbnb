from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new amenity"""
        data = api.payload
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        if not data.get('name'):
            return {'error': 'Name cannot be empty'}, 400
        try:
            amenity = facade.create_amenity(data)
            return {'id': amenity.id, 'name': amenity.name}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Lister toutes les amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity found')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """amenity ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity by ID"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        data = api.payload
        if facade.get_amenity(amenity_id) == None:
            return {'error': 'Amenity not found'}, 404
        if not data.get('name'):
            return {'error': 'Name cannot be empty'}, 400
        try:
            updated = facade.update_amenity(amenity_id, api.payload)
            return {'message': 'Amenity updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
