#!/usr/bin/python3
"""
    This module defines the Amenity Class for the AirBnB clone
"""
from model.base import BaseModel


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
    __required = ('name', )

    def __init__(self, name):
        BaseModel.__init__(self)
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if type(name) is not str:
            raise TypeError('name must be a string')
        self.__name = name
