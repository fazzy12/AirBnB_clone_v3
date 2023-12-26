#!/usr/bin/python3
"""API setup and configuration"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State

# Retrieve all State objects


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects."""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

# Retrieve a specific State object by ID


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by its ID."""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)

# Delete a specific State object by ID


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by its ID."""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)

# Create a new State object


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object."""
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    if "name" not in json_data:
        abort(400, "Missing name")
    new_state = State(**json_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

# Update a specific State object by ID


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by its ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())
