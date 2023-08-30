#!/usr/bin/python3
"""
    Tests for City class
"""

import unittest
from model.city import City
from model.country import Country
from model.base import BaseModel


class TestCity(unittest.TestCase):
    """ Tests for the City class """
    def setUp(self):
        country = Country('Uruguay', 'UY')
        self.city = City('Montevideo', country.id)
    
    def test_inheritance(self):
        self.assertIsInstance(self.city, BaseModel)
        self.assertIsInstance(self.city, City)
        self.assertEqual(type(self.city), City)

    def test_attrs(self):
        city = self.city
        self.assertTrue(hasattr(city, 'id'))
        self.assertTrue(hasattr(city, 'created_at'))
        self.assertTrue(hasattr(city, 'updated_at'))
        self.assertTrue(hasattr(city, 'name'))

    def test_mandatory_fields(self):
        with self.assertRaises(TypeError):
            city = City()

    def test_inherited_methods(self):
        city = self.city
        city_dict = city.to_dict()
        self.assertEqual(city_dict.get('__class__'), type(city).__name__)
        self.assertEqual(city_dict.get('name'), city.name)

    def test_city_constructor(self):
        city = self.city
        new = city.constructor(city.to_dict())
        self.assertEqual(city, new)
