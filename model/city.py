#!/usr/bin/python3
"""
    This module defines the City class for the AirBnB clone
"""

from model.base import BaseModel
from datetime import datetime

class City(BaseModel):
    """
        Country Class for AirBnB 
        Attrs:
            - id (string): UUID4 
            - created_at (datetime): datetime of creation
            - updated_at (datetime): datetime of last update
            - name (string): name of the city
            - country (string): Country ID
    """

    def __init__(self, name, country):
        BaseModel.__init__(self)
        self.name = name
        self.country = country

    @classmethod
    def constructor(cls, dictionary):
        required = {
            'name': dictionary.get('name'),
            'country': dictionary.get('country')
            }

        new_city = cls(**required)
        keys = dictionary.keys()

        if '__class__' in keys:
            del dictionary['__class__']

        if 'created_at' in keys and type(dictionary['created_at']) is datetime:
            dictionary['created_at'] = \
                datetime.fromisoformat(dictionary['created_at'])

        if 'updated_at' in keys and type(dictionary['updated_at']) is datetime:
            dictionary['updated_at'] = \
                datetime.fromisoformat(dictionary['updated_at'])

        new_city.__dict__.update(dictionary)
        return new_city
