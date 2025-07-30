# app/api/v1/places.py

from flask_restx import Namespace, Resource, fields
from flask import request, abort
from app.models.place import Place # Importez le modèle Place
from app.models.user import User # Pour valider user_id et afficher l'hôte
from app.models.city import City # Pour valider city_id et afficher la ville
from app.models.amenity import Amenity # Pour gérer les amenities
from app import db # Importez l'instance de db

api = Namespace('places', description='Opérations liées aux lieux (places)')

# --- Modèles de sérialisation (sortie JSON) ---

# Modèle imbriqué pour afficher un résumé de l'hôte (User)
user_summary_model = api.model('UserSummary', {
    'id': fields.String(readOnly=True),
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String
})

# Modèle imbriqué pour afficher un résumé de la ville (City)
city_summary_model = api.model('CitySummary', {
    'id': fields.String(readOnly=True),
    'name': fields.String
})

# Modèle imbriqué pour afficher un résumé des équipements (Amenity)
amenity_summary_model = api.model('AmenitySummary', {
    'id': fields.String(readOnly=True),
    'name': fields.String
})

# Modèle principal pour la sérialisation d'un Place
place_model = api.model('Place', {
    'id': fields.String(readOnly=True, description='Identifiant unique du lieu'),
    'user_id': fields.String(required=True, description='ID de l\'hôte (utilisateur)'),
    'city_id': fields.String(required=True, description='ID de la ville'),
    'name': fields.String(required=True, description='Nom du lieu'),
    'description': fields.String(description='Description du lieu'),
    'number_rooms': fields.Integer(required=True, description='Nombre de chambres'),
    'number_bathrooms': fields.Integer(required=True, description='Nombre de salles de bain'),
    'max_guest': fields.Integer(required=True, description='Nombre maximum d\'invités'),
    'price_by_night': fields.Integer(required=True, description='Prix par nuit'),
    'latitude': fields.Float(description='Latitude géographique'),
    'longitude': fields.Float(description='Longitude géographique'),
    'created_at': fields.DateTime(readOnly=True, description='Date de création'),
    'updated_at': fields.DateTime(readOnly=True, description='Date de dernière mise à jour'),

    # Relations imbriquées pour une meilleure lisibilité
    # Ces champs seront remplis par les setters/getters du modèle Place ou par votre logique
    # Il est crucial que vos modèles Place, User, City, Amenity aient les relations définies
    # Par exemple dans Place:
    # host = db.relationship('User', backref='places', lazy=True)
    # city = db.relationship('City', backref='places', lazy=True)
    # amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy=True), lazy='dynamic')
    'host': fields.Nested(user_summary_model, description='Détails de l\'hôte', attribute='host', skip_none=True),
    'city': fields.Nested(city_summary_model, description='Détails de la ville', attribute='city', skip_none=True),
    'amenities': fields.List(fields.Nested(amenity_summary_model), description='Liste des équipements associés', attribute='amenities', skip_none=True)
})

# --- Parsers pour la validation des entrées (payload des requêtes) ---

# Parser pour la création d'un Place (tous les champs non-nullables requis)
place_create_parser = api.parser()
place_create_parser.add_argument('user_id', type=str, required=True, help='ID de l\'hôte (utilisateur)', location='json')
place_create_parser.add_argument('city_id', type=str, required=True, help='ID de la ville', location='json')
place_create_parser.add_argument('name', type=str, required=True, help='Nom du lieu', location='json')
place_create_parser.add_argument('description', type=str, help='Description du lieu', location='json')
place_create_parser.add_argument('number_rooms', type=int, required=True, help='Nombre de chambres', location='json')
place_create_parser.add_argument('number_bathrooms', type=int, required=True, help='Nombre de salles de bain', location='json')
place_create_parser.add_argument('max_guest', type=int, required=True, help='Nombre maximum d\'invités', location='json')
place_create_parser.add_argument('price_by_night', type=int, required=True, help='Prix par nuit', location='json')
place_create_parser.add_argument('latitude', type=float, help='Latitude géographique', location='json')
place_create_parser.add_argument('longitude', type=float, help='Longitude géographique', location='json')
place_create_parser.add_argument('amenity_ids', type=list, default=[], help='Liste des IDs des équipements', location='json') # Pour associer des amenities

# Parser pour la mise à jour d'un Place (tous les champs optionnels)
place_update_parser = api.parser()
place_update_parser.add_argument('user_id', type=str, help='ID de l\'hôte (utilisateur)', location='json')
place_update_parser.add_argument('city_id', type=str, help='ID de la ville', location='json')
place_update_parser.add_argument('name', type=str, help='Nom du lieu', location='json')
place_update_parser.add_argument('description', type=str, help='Description du lieu', location='json')
place_update_parser.add_argument('number_rooms', type=int, help='Nombre de chambres', location='json')
place_update_parser.add_argument('number_bathrooms', type=int, help='Nombre de salles de bain', location='json')
place_update_parser.add_argument('max_guest', type=int, help='Nombre maximum d\'invités', location='json')
place_update_parser.add_argument('price_by_night', type=int, help='Prix par nuit', location='json')
place_update_parser.add_argument('latitude', type=float, help='Latitude géographique', location='json')
place_update_parser.add_argument('longitude', type=float, help='Longitude géographique', location='json')
place_update_parser.add_argument('amenity_ids', type=list, help='Liste des IDs des équipements à (re)associer', location='json')


# --- Ressources de l'API ---

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_model, code=200)
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
                "owner_id": new_place.owner_id
                }, 201
        except ValueError as e:
            return  {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Récupère la liste de tous les lieux."""
        places = Place.query.all()
        return places

    @api.doc('create_place')
    @api.expect(place_create_parser)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Crée un nouveau lieu."""
        data = place_create_parser.parse_args()

        # Validation des IDs de clé étrangère
        user = User.query.get(data['user_id'])
        if not user:
            api.abort(400, message=f"User with ID {data['user_id']} not found.")
        city = City.query.get(data['city_id'])
        if not city:
            api.abort(400, message=f"City with ID {data['city_id']} not found.")

        # Récupération des objets Amenity
        amenities = []
        if data['amenity_ids']:
            for amenity_id in data['amenity_ids']:
                amenity = Amenity.query.get(amenity_id)
                if not amenity:
                    api.abort(400, message=f"Amenity with ID {amenity_id} not found.")
                amenities.append(amenity)

        try:
            new_place = Place(
                user_id=data['user_id'],
                city_id=data['city_id'],
                name=data['name'],
                description=data.get('description'),
                number_rooms=data['number_rooms'],
                number_bathrooms=data['number_bathrooms'],
                max_guest=data['max_guest'],
                price_by_night=data['price_by_night'],
                latitude=data.get('latitude'),
                longitude=data.get('longitude')
            )
            # Ajouter les amenities si la relation est définie sur le modèle Place
            if amenities:
                new_place.amenities = amenities # Ceci suppose que la relation 'amenities' est définie sur le modèle Place

            new_place.save()
            return new_place, 201

        except ValueError as e:
            api.abort(400, message=str(e))
        except Exception as e:
            db.session.rollback() # En cas d'erreur, annulez la transaction
            api.abort(500, message=f"Une erreur interne est survenue: {str(e)}")


@api.route('/<string:place_id>')
@api.response(404, 'Lieu non trouvé')
@api.param('place_id', 'L\'identifiant du lieu')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Récupère les détails d'un lieu spécifique."""
        place = Place.query.get(place_id)
        if not place:
            api.abort(404, message="Lieu non trouvé")
        return place

    @api.doc('update_place')
    @api.expect(place_update_parser)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Met à jour un lieu existant."""
        place = Place.query.get(place_id)
        if not place:
            api.abort(404, message="Lieu non trouvé")

        data = place_update_parser.parse_args()

        # Validation et mise à jour des IDs de clé étrangère si fournis
        if 'user_id' in data and data['user_id'] is not None:
            user = User.query.get(data['user_id'])
            if not user:
                api.abort(400, message=f"User with ID {data['user_id']} not found.")
            place.user_id = data['user_id']
        if 'city_id' in data and data['city_id'] is not None:
            city = City.query.get(data['city_id'])
            if not city:
                api.abort(400, message=f"City with ID {data['city_id']} not found.")
            place.city_id = data['city_id']

        # Mise à jour des autres champs
        if 'name' in data and data['name'] is not None:
            place.name = data['name']
        if 'description' in data and data['description'] is not None:
            place.description = data['description']
        if 'number_rooms' in data and data['number_rooms'] is not None:
            place.number_rooms = data['number_rooms']
        if 'number_bathrooms' in data and data['number_bathrooms'] is not None:
            place.number_bathrooms = data['number_bathrooms']
        if 'max_guest' in data and data['max_guest'] is not None:
            place.max_guest = data['max_guest']
        if 'price_by_night' in data and data['price_by_night'] is not None:
            place.price_by_night = data['price_by_night']
        if 'latitude' in data and data['latitude'] is not None:
            place.latitude = data['latitude']
        if 'longitude' in data and data['longitude'] is not None:
            place.longitude = data['longitude']

        # Gestion des amenities (relation Many-to-Many)
        if 'amenity_ids' in data and data['amenity_ids'] is not None:
            new_amenities = []
            for amenity_id in data['amenity_ids']:
                amenity = Amenity.query.get(amenity_id)
                if not amenity:
                    api.abort(400, message=f"Amenity with ID {amenity_id} not found.")
                new_amenities.append(amenity)
            place.amenities = new_amenities # Met à jour la liste des amenities

        try:
            place.save()
            return place
        except ValueError as e:
            api.abort(400, message=str(e))
        except Exception as e:
            db.session.rollback()
            api.abort(500, message=f"Une erreur interne est survenue lors de la mise à jour: {str(e)}")

    @api.doc('delete_place')
    @api.response(204, 'Lieu supprimé avec succès')
    def delete(self, place_id):
        """Supprime un lieu."""
        place = Place.query.get(place_id)
        if not place:
            api.abort(404, message="Lieu non trouvé")

        try:
            place.delete()
            return '', 204
        except Exception as e:
            db.session.rollback()
            api.abort(500, message=f"Une erreur interne est survenue lors de la suppression: {str(e)}")
