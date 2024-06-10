#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""

from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches for Place objects based on the JSON in the request body"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        places = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state is not None:
                places.extend(state.places)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city is not None:
                places.extend(city.places)

        places = list(set(places))  # Remove duplicates

        if amenities:
            places = [place for place in places
                      if all(amenity_id in place.amenities
                             for amenity_id in amenities)]

    return jsonify([place.to_dict() for place in places])
