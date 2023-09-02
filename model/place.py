#!/usr/bin/python3
"""
    This module defines the Place Class for the AirBnB clone
"""
from model.base import BaseModel


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
            - country (string): country (ID) in which the place is located
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
    __required = (
        'name', 'description', 'address', 'city', 'country',
        'latitude', 'longitude', 'host', 'price_per_night',
        'max_guests', 'number_rooms', 'number_bathrooms',
        'amenities', 'reviews'
    )

    def __init__(self, name, address,
                 host, price_per_night,
                 number_rooms, number_bathrooms,
                 city, country,
                 max_guests, amenities=[], description='',
                 latitude=0, longitude=0, reviews=[]):
        
        BaseModel.__init__(self)
        self.__name = name
        self.__description = description
        self.__address = address
        self.__latitude = latitude
        self.__longitude = longitude
        self.__city = city
        self.__country = country
        self.__host = host
        self.__price_per_night = price_per_night
        self.__max_guests = max_guests
        self.__number_rooms = number_rooms
        self.__number_bathrooms = number_bathrooms
        self.__amenities = amenities
        self.__reviews = reviews

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if type(name) is not str:
            raise TypeError('place name must be a string')
        self.__name = name

    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, description):
        if type(description) is not str:
            raise TypeError('place description must be a string')
        self.__description = description

    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, address):
        if type(address) is not str:
            raise TypeError('place address must be a string')
        self.__address = address

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, latitude):
        if type(latitude) is not float:
            raise TypeError('place latitude must be a float')
        self.__latitude = latitude

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, longitude):
        if type(longitude) is not float:
            raise TypeError('place longitude must be a float')
        self.__longitude = longitude

    @property
    def city(self):
        return self.__city
    
    @city.setter
    def city(self, city):
        if type(city) is not str:
            raise TypeError('place city must be a string')
        self.__city = city

    @property
    def country(self):
        return self.__country
    
    @country.setter
    def country(self, country):
        if type(country) is not str:
            raise TypeError('place country must be a string')
        self.__country = country

    @property
    def host(self):
        return self.__host
    
    @host.setter
    def host(self, host):
        if type(host) is not str:
            raise TypeError('place host must be a string')
        self.__host = host

    @property
    def price_per_night(self):
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, price_per_night):
        if type(price_per_night) is not int:
            raise TypeError('place price_per_night must be an int')
        if price_per_night < 0:
            raise AttributeError("price_per_night can't be negative")
        self.__price_per_night = price_per_night

    @property
    def max_guests(self):
        return self.__max_guests

    @max_guests.setter
    def max_guests(self, max_guests):
        if type(max_guests) is not int:
            raise TypeError('place max_guests must be an int')
        if max_guests < 0:
            raise AttributeError("max_guests can't be negative")
        self.__max_guests = max_guests

    @property
    def number_rooms(self):
        return self.__number_rooms

    @number_rooms.setter
    def number_rooms(self, number_rooms):
        if type(number_rooms) is not int:
            raise TypeError('place number_rooms must be an int')
        if number_rooms < 0:
            raise AttributeError("number_rooms can't be negative")
        self.__number_rooms = number_rooms

    @property
    def number_bathrooms(self):
        return self.__number_bathrooms

    @number_bathrooms.setter
    def number_bathrooms(self, number_bathrooms):
        if type(number_bathrooms) is not int:
            raise TypeError('place number_bathrooms must be an int')
        if number_bathrooms < 0:
            raise AttributeError("number_bathrooms can't be negative")
        self.__number_bathrooms = number_bathrooms

    @property
    def amenities(self):
        return self.__amenities
    
    @amenities.setter
    def amenities(self, amenities):
        if type(amenities) is not list or \
            not all(type(amenity) is str for amenity in amenities):
            raise TypeError('amenities must be a list of amenity IDs')

    @property
    def reviews(self):
        return self.__reviews
    
    @reviews.setter
    def reviews(self, reviews):
        if type(reviews) is not list or \
            not all(type(review) is str for review in reviews):
            raise TypeError('place reviews must be a string')
        self.__reviews = reviews
