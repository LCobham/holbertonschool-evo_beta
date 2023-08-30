#!/usr/bin/python3
"""
    This module defines the Place Class for the AirBnB clone
"""
from model.base import BaseModel
from datetime import datetime


class Place(BaseModel):
    """ Place Class for AirBnB 
        Attrs:
            - id (string): UUID4 
            - created_at (datetime): datetime of creation
            - updated_at (datetime): datetime of last update
            - name (string): name of the place
            - description (string): brief description from the owner
            - address (string): place address
            - city (string): city (ID) in which is located
            - ountry (string): country (ID) in which the place is located
            - longitude (float): longitude
            - latitude (float): latitude
            - host (string): user ID of the owner of the place
            - price_per_night (int): price in U$S per night
            - number_rooms (int): number of bedrooms in the place
            - number_bathrooms (int): number of bathrooms in the place
            - max_guests (int): maximum number of guests the host allows
            - amenities (list): list of available amenities' ID
            - reviews (list): list of review IDs by other users
        
        Methods:
            - constructor: Recreate a User object from a dictionary
            previously obtained with the `to_dict()` method
    """

    def __init__(self, name, address,
                 host, price_per_night,
                 number_rooms, number_bathrooms,
                 city, country,
                 max_guests, amenities=[], description='',
                 latitude=0, longitude=0):
        
        BaseModel.__init__(self)
        self.name = name
        self.description = description
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.country = country
        self.host = host
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.number_rooms = number_rooms
        self.number_bathrooms = number_bathrooms
        self.amenities = amenities
        
        # Initiated empty because Places have no reviews when created
        self.reviews = []

    @classmethod
    def constructor(cls, dictionary):
        required = {
            'name': dictionary.get('name'),
            'address': dictionary.get('address'),
            'host': dictionary.get('host'),
            'price_per_night': dictionary.get('price_per_night'),
            'number_rooms': dictionary.get('number_rooms'),
            'number_bathrooms': dictionary.get('number_bathrooms'),
            'max_guests': dictionary.get('max_guests'),
            'city': dictionary.get('city'),
            'country': dictionary.get('country')
            }

        new_place = cls(**required)
        keys = dictionary.keys()

        if '__class__' in keys:
            del dictionary['__class__']

        if 'created_at' in keys and type(dictionary['created_at']) is datetime:
            dictionary['created_at'] = \
                datetime.fromisoformat(dictionary['created_at'])

        if 'updated_at' in keys and type(dictionary['updated_at']) is datetime:
            dictionary['updated_at'] = \
                datetime.fromisoformat(dictionary['updated_at'])

        new_place.__dict__.update(dictionary)
        return new_place
