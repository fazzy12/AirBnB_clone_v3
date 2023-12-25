#!/usr/bin/python3
""" Blueprint for API v1 """

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# This is intentionally left empty for wildcard imports.
# Wildcard imports are discouraged by PEP8 but are okay for this use-case.
