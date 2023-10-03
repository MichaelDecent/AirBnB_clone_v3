#!/usr/bin/python3
"""
This Module contains Place objects that
handles all default RESTFul API actions
"""
from flask import request, abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places_list = [place.to_dict() for place in city.places]

    return jsonify(places_list)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a place based on its ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Delete a place ob based on its ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_places(city_id):
    """
    Create a place for a particular ID
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, 'Not a JSON')

    required_keys = ['user_id', 'name']
    if required_keys[0] not in json_request:
        abort(400, 'Missing user_id')
    if storage.get(User, json_request['user_id']) is None:
        abort(404)
    if required_keys[1] not in json_request:
        abort(400, 'Missing name')
    place = Place(city_id=city_id, **json_request)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Updated a place attributes based on its ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in json_request.items():
        if key is not ignore_keys:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def place_search():
    json_request = request.get_json()
    if not json_request:
        abort(404)
    
    check_key = 0
    for val in json_request.values():
        if len(val) != 0:
            check_key = 1
            break

    if len(json_request) == 0 or check_key == 0:
        places = storage.all(Place)
        places_list = [place.to_dict() for place in places.values()]
        return jsonify(places_list)

    print (json_request)
    places_list = []
    amenities_list = [obj.to_dict() for obj in storage.all(Amenity).values()]
    for key, value in json_request.items():
        if key == "states" and len(value) != 0:
            for id in value:
                state = storage.get(State, id)
                if state is None:
                    abort(404)
                for city in state.cities:
                    for place in city.places:
                        places_list.append(place.to_dict())

        if key == "cities" and len(value) != 0:
            for id in value:
                city = storage.get(City, id)
                if city is None:
                    abort(404)
                for place in city.places:
                    places_list.append(place.to_dict())
        
        if key == "amenities" and len(value) != 0 and len(places_list) == 0:
            list_places = [place for place in storage.all(Place).values()]
            for place in list_places:
                for amenity in amenities_list:
                    if amenity in place.amenities:
                        places_list.append(place.to_dict())

    return jsonify(places_list)             