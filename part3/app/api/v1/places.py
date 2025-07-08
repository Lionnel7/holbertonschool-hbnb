from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        place_data = api.payload
        if not place_data:
            return {'error': 'empty data'}, 400
        current_user = get_jwt_identity()
        place_data["owner_id"] = current_user["id"]
        try:
            new_place = facade.create_place(place_data)
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner.id
                }, 201
        except ValueError as e:
            return  {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        list_all = []
        place = facade.get_all_places()
        for element in place:
            list_all.append({
                "id": element.id,
                "title": element.title,
                "latitude": element.latitude,
                "longitude": element.longitude,
                })
        return list_all, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'No place found'}, 404
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        """Get user details by ID"""
        new_data = api.payload
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'place not found'}, 404
        elif place.owner.id != current_user["id"]:
            return {'error': 'Unauthorized action'}, 403
        try:
            facade.update_place(place_id=place_id, place_data=new_data)
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            return  {'error': str(e)}, 400