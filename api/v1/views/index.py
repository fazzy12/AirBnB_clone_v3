#!/usr/bin/python3
""" Index route for API v1 """

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ Return API status """
    return jsonify({"status": "OK"})
