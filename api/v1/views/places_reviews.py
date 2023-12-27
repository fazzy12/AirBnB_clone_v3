#!/usr/bin/python3
"""Places Reviews module"""
from flask import jsonify, request, abort
from models import Review, Place, User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = Review.get(review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = Review.get(review_id)
    if not review:
        abort(404)
    review.delete()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    user_id = data.get('user_id')
    if not user_id or not User.get(user_id):
        abort(404 if not user_id else 400, "Missing user_id")

    text = data.get('text')
    if not text:
        abort(400, "Missing text")

    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = Review.get(review_id)
    if not review:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id',
                       'user_id',
                       'place_id',
                       'created_at',
                       'updated_at']:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
