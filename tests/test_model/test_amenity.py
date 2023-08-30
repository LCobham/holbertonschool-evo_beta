#!/usr/bin/python3
"""
    Tests for Amenity class
"""

import unittest
from model.amenity import Amenity
from model.base import BaseModel


class TestAmenity(unittest.TestCase):
    """ Tests for the Amenity class """
    def setUp(self):
        self.amenity = Amenity('WiFi')
    
    def test_inheritance(self):
        self.assertIsInstance(self.amenity, BaseModel)
        self.assertIsInstance(self.amenity, Amenity)
        self.assertEqual(type(self.amenity), Amenity)

    def test_attrs(self):
        am = self.amenity
        self.assertTrue(hasattr(am, 'id'))
        self.assertTrue(hasattr(am, 'created_at'))
        self.assertTrue(hasattr(am, 'updated_at'))
        self.assertTrue(hasattr(am, 'name'))

    def test_mandatory_fields(self):
        with self.assertRaises(TypeError):
            am = Amenity()

    def test_inherited_methods(self):
        am = self.amenity
        am_dict = am.to_dict()
        self.assertEqual(am_dict.get('__class__'), type(am).__name__)
        self.assertEqual(am_dict.get('name'), am.name)

    def test_amenity_constructor(self):
        am = self.amenity
        new = Amenity.constructor(am.to_dict())
        self.assertEqual(am, new)
