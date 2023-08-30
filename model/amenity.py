#!/usr/bin/python3
"""
    This module defines the Amenity Class for the AirBnB clone
"""
from model.base import BaseModel
from datetime import datetime


class Amenity(BaseModel):
    """ 
        Amenity class for AirBnB clone
        Attrs:
            - id (string): UUID4 
            - created_at (datetime): datetime of creation
            - updated_at (datetime): datetime of last update
            - name (string): name of amenity
        
        Methods:
            - constructor: Recreate a User object from a dictionary
            previously obtained with the `to_dict()` method
    """
    def __init__(self, name):
        BaseModel.__init__(self)
        self.name = name

    @classmethod
    def constructor(cls, dictionary):
        required = {
            'name': dictionary.get('name')
            }

        new_amenity = cls(**required)
        keys = dictionary.keys()

        if '__class__' in keys:
            del dictionary['__class__']

        if 'created_at' in keys and type(dictionary['created_at']) is datetime:
            dictionary['created_at'] = \
                datetime.fromisoformat(dictionary['created_at'])

        if 'updated_at' in keys and type(dictionary['updated_at']) is datetime:
            dictionary['updated_at'] = \
                datetime.fromisoformat(dictionary['updated_at'])

        new_amenity.__dict__.update(dictionary)
        return new_amenity
