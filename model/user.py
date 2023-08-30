#!/usr/bin/python3
"""
    This module defines the User Class for the AirBnB clone
"""
from model.base import BaseModel
from datetime import datetime


class User(BaseModel):
    """ User Class for AirBnB 
        Attrs:
            - id (string): UUID4 
            - created_at (datetime): datetime of creation
            - updated_at (datetime): datetime of last update
            - email (string): email of the user
            - password (string): user password
            - first_name (string): User's first name
            - last_name (string): User's last name
        
        Methods:
            - constructor: Recreate a User object from a dictionary
            previously obtained with the `to_dict()` method
    """

    def __init__(self, email, password, first_name='', last_name=''):
        BaseModel.__init__(self)
        if not email or not password:
            raise AttributeError('email or password missing')

        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def constructor(cls, dictionary):
        required = {
            'email': dictionary.get('email'),
            'password': dictionary.get('password')
            }

        new_user = cls(**required)
        keys = dictionary.keys()

        if '__class__' in keys:
            del dictionary['__class__']

        if 'created_at' in keys and type(dictionary['created_at']) is datetime:
            dictionary['created_at'] = \
                datetime.fromisoformat(dictionary['created_at'])

        if 'updated_at' in keys and type(dictionary['updated_at']) is datetime:
            dictionary['updated_at'] = \
                datetime.fromisoformat(dictionary['updated_at'])

        new_user.__dict__.update(dictionary)
        return new_user
