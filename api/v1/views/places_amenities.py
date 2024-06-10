#!/usr/bin/python3
"""
view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_of_place(place_id):
    """Retrieves the list of all Amenity objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    return jsonify([storage.get(Amenity, amenity_id).to_dict()
                    for amenity_id in place.amenity_ids])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes a Amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def add_amenity_to_a_place(place_id, amenity_id):
    """Creates a Amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
