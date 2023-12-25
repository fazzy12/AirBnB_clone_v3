#!/usr/bin/python3
""" API setup and configuration """

import os
from flask import Flask, jsonify
# from flask_cors import CORS

from models import storage
from api.v1.views import app_views


app = Flask(__name__)


@app.teardown_appcontext
def teardown_flask(exception):
    '''The Flask app/request context end event listener.'''
    storage.close()


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
