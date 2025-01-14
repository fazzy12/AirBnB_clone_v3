#!/usr/bin/python3
"""API setup and configuration"""

import os
from flask import Flask, jsonify, abort
from flask_cors import CORS

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_flask(exception):
    """ The Flask app/request context end event listener. """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ 404 error handler. """
    return jsonify(error="Not found"), 404


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
