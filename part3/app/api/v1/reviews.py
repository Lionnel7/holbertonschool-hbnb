from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='Place ID'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'comment': fields.String(required=True, description='Text of review')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new review"""
        review_data = api.payload
        current_user = get_jwt_identity()
        place = facade.get_place(review_data["place_id"])
        if not place: 
            return {'error': 'wrong place id'}, 400
        if place.owner_id == current_user["id"]:
            return {'error': 'You cannot review your own place.'}, 400
        for review in place.reviews:
            if review.user_id == current_user["id"]:
                return {'error': 'You have already reviewed this place.'}, 400
        try:
            review_data["user_id"] = current_user["id"]
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Retrieve review details by ID"""
        review = facade.get_review(review_id)
        if review:
            return review.to_dict(), 200
        else:
            return {'error': 'Review not found'}, 404
        

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update review information"""
        review_data = api.payload
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        elif current_user["id"] != review.user_id:
            return {'error': "Unauthorized action."}, 403
        try:
            facade.update_review(review_id, review_data)
            return review.to_dict(), 200
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        elif current_user["id"] != review.user_id:
            return {'error': "Unauthorized action."}, 403
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        output = []
        place_reviews = facade.get_reviews_by_place(place_id)
        if place_reviews is None:
            return {'error': 'Place not found'}, 404
        for element in place_reviews:
            output.append(element.to_dict())
        return output, 200
