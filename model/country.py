#!/usr/bin/python3
"""
    This module defines the Country class for the
    AirBnB clone
"""

from model.base import BaseModel


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
    __required = ('name', 'iso', 'cities')

    def __init__(self, name, iso, cities=[]):
        BaseModel.__init__(self)
        self.__name = name
        self.__iso = iso
        self.__cities = cities

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, country_name):
        if type(country_name) is not str:
            raise TypeError('country name must be a string')
        self.__name = country_name

    @property
    def iso(self):
        return self.__iso

    @iso.setter
    def iso(self, iso_code):
        if type(iso_code) is not str:
            raise TypeError('iso code must be a string')
        if len(iso_code) != 2:
            raise AttributeError('iso code must be a two digit alpha code')
        self.__iso = iso_code.upper()

    @property
    def cities(self):
        return self.__cities

    @cities.setter
    def cities(self, cities):
        if type(cities) is not list or \
                not all(type(city) is str for city in cities):
            raise TypeError('cities must be a list of city IDs (string)')
        self.__cities = cities
