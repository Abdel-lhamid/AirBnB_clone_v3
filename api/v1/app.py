#!/usr/bin/python3
"""API for AirBnB_clone_v3"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = int(os.getenv('HBNB_API_PORT', 5000))
CORS(app, resources={'/*': {'origins': host}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found_404(error):
    """returns json format with 404 HTTP error code page not found."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def handle_error_400(error):
    """handles error 400"""
    if isinstance(error, Exception) and hasattr(error, 'description'):
        return jsonify({"error": error.description}), 400
    return jsonify({"error": "Bad request"}), 400


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
