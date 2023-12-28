#!/usr/bin/python3
"""Places view module"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places based on criteria"""
    criteria = request.get_json()

    if not criteria:
        abort(400, "Not a JSON")

    places = storage.all(Place).values()

    if 'states' in criteria:
        states = criteria['states']
        places = [p for p in places if p.city.state_id in states]

    if 'cities' in criteria:
        cities = criteria['cities']
        places = [p for p in places if p.city_id in cities]

    if 'amenities' in criteria:
        amenities = criteria['amenities']
        places = [p for p in places if all(
            amenity_id in [a.id for a in p.amenities] for amenity_id in amenities)]

    return jsonify([place.to_dict() for place in places]), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieve all Place objects for a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a specific Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req_json = request.get_json()
    if not req_json:
        abort(400, "Not a JSON")
    if "user_id" not in req_json:
        abort(400, "Missing user_id")
    if storage.get(User, req_json["user_id"]) is None:
        abort(404)
    if "name" not in req_json:
        abort(400, "Missing name")
    new_place = Place(**req_json)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req_json = request.get_json()
    if not req_json:
        abort(400, "Not a JSON")
    for key, value in req_json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
