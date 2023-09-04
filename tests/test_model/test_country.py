#!/usr/bin/python3
"""
    Tests for Country class
"""

import unittest
from model.country import Country
from model.base import BaseModel


class TestCountry(unittest.TestCase):
    """ Tests for the Country class """
    def setUp(self):
        self.country = Country('Uruguay', 'UY')

    def test_inheritance(self):
        self.assertIsInstance(self.country, BaseModel)
        self.assertIsInstance(self.country, Country)
        self.assertEqual(type(self.country), Country)

    def test_attrs(self):
        country = self.country
        self.assertTrue(hasattr(country, 'id'))
        self.assertTrue(hasattr(country, 'created_at'))
        self.assertTrue(hasattr(country, 'updated_at'))
        self.assertTrue(hasattr(country, 'name'))

    def test_mandatory_fields(self):
        with self.assertRaises(TypeError):
            Country()

    def test_setters(self):
        with self.assertRaises(TypeError):
            self.country.name = 22

        with self.assertRaises(TypeError):
            self.country.iso = (1, 2, 3)

        with self.assertRaises(AttributeError):
            self.country.iso = 'STRING IS TOO LONG'

    def test_inherited_methods(self):
        country = self.country
        country_dict = country.to_dict()
        self.assertEqual(country_dict.get('__class__'), type(country).__name__)
        self.assertEqual(country_dict.get('name'), country.name)

    def test_country_constructor(self):
        country = self.country
        new = Country.constructor(country.to_dict())
        self.assertEqual(country, new)
