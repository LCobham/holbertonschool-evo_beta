#!/usr/bin/python3
"""
    This module defines the Country class for the
    AirBnB clone
"""

from model.base import BaseModel
from datetime import datetime


class Country(BaseModel):
    """
        Country Class for AirBnB 
        Attrs:
            - id (string): UUID4 
            - created_at (datetime): datetime of creation
            - updated_at (datetime): datetime of last update
            - name (string): name of the country
            - iso (string): two letter code based on ISO 3166 Alpha-2
            - cities (list): list of registered cities in the country
    """

    def __init__(self, name, iso):
        BaseModel.__init__(self)
        self.name = name
        self.iso = iso

        # When first created, no cities are registered in that country
        self.cities = []

    @classmethod
    def constructor(cls, dictionary):
        required = {
            'name': dictionary.get('name'),
            'iso': dictionary.get('iso')
            }

        new_country = cls(**required)
        keys = dictionary.keys()

        if '__class__' in keys:
            del dictionary['__class__']

        if 'created_at' in keys and type(dictionary['created_at']) is datetime:
            dictionary['created_at'] = \
                datetime.fromisoformat(dictionary['created_at'])

        if 'updated_at' in keys and type(dictionary['updated_at']) is datetime:
            dictionary['updated_at'] = \
                datetime.fromisoformat(dictionary['updated_at'])

        new_country.__dict__.update(dictionary)
        return new_country
