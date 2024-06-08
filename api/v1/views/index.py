#!/usr/bin/python3
"""App views for AirBnB_clone_v3"""
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Route to status page"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    """retrieves the number of each objects by type"""
    total_count = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "State": "states",
               "Review": "reviews",
               "User": "users"}
    for cls in classes:
        count = storage.count(cls)
        total_count[classes.get(cls)] = count
    return jsonify(total_count)
