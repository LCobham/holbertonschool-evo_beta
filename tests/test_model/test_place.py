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
        john = User("jdoe@mail.com", "password")
        wifi = Amenity("WiFi")
        country = Country('Uruguay', 'UY')
        city = City('Mercedes', country.id)
        inputs = {
            'name': 'House by the beach',
            'address': 'Ocean Drive 1234',
            'host': john.dict_key,
            'city': city.dict_key,
            'country': country.dict_key,
            'price_per_night': 120,
            'number_rooms': 2,
            'number_bathrooms': 1,
            'max_guests': 3,
            'amenities': [wifi.dict_key]
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
            place = Place()

    def test_inherited_methods(self):
        place = self.place
        place_dict = place.to_dict()
        self.assertEqual(place_dict.get('__class__'), type(place).__name__)
        self.assertEqual(place_dict.get('id'), place.id)

    def test_place_constructor(self):
        place = self.place
        new = Place.constructor(place.to_dict())
        self.assertEqual(place, new)
