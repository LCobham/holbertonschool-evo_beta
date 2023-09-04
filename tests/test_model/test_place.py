#!/usr/bin/python3
"""
    Tests for Place class
"""

import unittest
from model.place import Place
from model.amenity import Amenity
from model.user import User
from model.country import Country
from model.city import City
from model.base import BaseModel


class TestPlace(unittest.TestCase):
    """ Tests for the Place class """
    def setUp(self):
        john = User("jdoe@mail.com", "password", "John", "Doe")
        wifi = Amenity("WiFi")
        country = Country('Uruguay', 'UY')
        city = City('Mercedes', country.id)
        inputs = {
            'name': 'House by the beach',
            'address': 'Ocean Drive 1234',
            'host': john.key,
            'city': city.key,
            'country': country.key,
            'price_per_night': 120,
            'number_rooms': 2,
            'number_bathrooms': 1,
            'max_guests': 3,
            'amenities': [wifi.key]
            }

        self.place = Place(**inputs)

    def test_inheritance(self):
        self.assertIsInstance(self.place, BaseModel)
        self.assertIsInstance(self.place, Place)
        self.assertEqual(type(self.place), Place)

    def test_attrs(self):
        place = self.place
        self.assertTrue(hasattr(place, 'id'))
        self.assertTrue(hasattr(place, 'created_at'))
        self.assertTrue(hasattr(place, 'updated_at'))

        atributes = (
            'name', 'description', 'address', 'latitude',
            'longitude', 'host', 'price_per_night', 'number_rooms',
            'number_bathrooms', 'max_guests', 'amenities', 'reviews'
        )
        for atr in atributes:
            self.assertTrue(hasattr(place, atr))

    def test_mandatory_fields(self):
        with self.assertRaises(TypeError):
            Place()

    def test_setters(self):
        with self.assertRaises(TypeError):
            self.place.name = 22

        with self.assertRaises(TypeError):
            self.place.description = (1, 2, 3)

        with self.assertRaises(TypeError):
            self.place.address = ['a list', 'of strings']

        with self.assertRaises(TypeError):
            self.place.host = set(['a', 2, 4, 1])

        with self.assertRaises(TypeError):
            self.place.latitude = 'string'

        with self.assertRaises(TypeError):
            self.place.longitude = 8

        with self.assertRaises(AttributeError):
            self.place.number_bathrooms = -3

        with self.assertRaises(TypeError):
            self.place.number_rooms = (1, 2, 3)

        with self.assertRaises(TypeError):
            self.place.max_guests = 'string'

        with self.assertRaises(TypeError):
            self.place.amenities = ('string', 'tuple')

        with self.assertRaises(TypeError):
            self.place.reviews = ('string', 'tuple')

    def test_inherited_methods(self):
        place = self.place
        place_dict = place.to_dict()
        self.assertEqual(place_dict.get('__class__'), type(place).__name__)
        self.assertEqual(place_dict.get('id'), place.id)

    def test_place_constructor(self):
        place = self.place
        new = Place.constructor(place.to_dict())
        self.assertEqual(place, new)
