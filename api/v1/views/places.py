#!/usr/bin/python3
"""Places view module"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, State, City, Amenity, Place
from os import getenv

HBNB_API_PORT = getenv('HBNB_API_PORT')


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending on the
    JSON in the body of the request.
    """
    req_json = request.get_json()

    if req_json is None or (
        not req_json.get('states') and
        not req_json.get('cities') and
        not req_json.get('amenities')
    ):
        obj_places = storage.all(Place)
        return jsonify([obj.to_dict() for obj in obj_places.values()])

    places = []

    if req_json.get('states'):
        obj_states = [storage.get(State, state_id)
                      for state_id in req_json['states']]
        for obj_state in obj_states:
            for obj_city in obj_state.cities:
                places.extend(obj_city.places)

    if req_json.get('cities'):
        obj_cities = [storage.get(City, city_id)
                      for city_id in req_json['cities']]
        for obj_city in obj_cities:
            places.extend(obj_city.places)

    if not places:
        places = storage.all(Place).values()

    if req_json.get('amenities'):
        obj_amenities = [storage.get(Amenity, amenity_id)
                         for amenity_id in req_json['amenities']]
        places = [place for place in places if all(
            amenity in place.amenities for amenity in obj_amenities)]

    return jsonify([obj.to_dict() for obj in places])


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
