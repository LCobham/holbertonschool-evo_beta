#!/usr/bin/python3
"""
    This module defines the City class for the AirBnB clone
"""

from model.base import BaseModel


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
    __required = ('name', 'country')

    def __init__(self, name, country):
        BaseModel.__init__(self)
        self.name = name
        self.country = country

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if type(name) is not str:
            raise TypeError('name must be a string')
        self.__name = name

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, country_id):
        if type(country_id) is not str:
            raise TypeError('country id must be a string')
        self.__country = country_id
