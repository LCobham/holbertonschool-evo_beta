#!/usr/bin/python3
"""
    Tests for the Abstract class
"""

from model.base import BaseModel
from abc import ABC
import unittest
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """ Tests for BaseModel class """

    def setUp(self):
        class Tmp(BaseModel):
            def __init__(self):
                BaseModel.__init__(self)

            def tmp_function(self):
                pass

            @classmethod
            def constructor(cls, dictionary):
                pass

        self.tmp = Tmp()
        self.tmp2 = Tmp()

    def test_no_direct_instanciation(self):
        with self.assertRaises(TypeError):
            model = BaseModel()

    def test_correct_attrs(self):
        self.assertEqual(type(self.tmp.id), str)
        self.assertEqual(type(self.tmp.created_at), datetime)
        self.assertEqual(self.tmp.created_at, self.tmp.updated_at)

    def test_inheritance(self):
        self.assertIsInstance(self.tmp, ABC)
        self.assertIsInstance(self.tmp, BaseModel)

    def test_to_dict(self):
        test_dict = self.tmp.to_dict()
        self.assertEqual(test_dict.get('id'), self.tmp.id)

        # Test new key is added with correct value
        self.assertEqual(str(test_dict.get('__class__')), 'Tmp')

        # Test datetime objects are converted to string
        self.assertEqual(test_dict.get('created_at'), str(self.tmp.created_at))
        self.assertEqual(test_dict.get('updated_at'), str(self.tmp.updated_at))

    def test_eq(self):
        self.assertFalse(self.tmp == self.tmp2)
        self.tmp2.id = self.tmp.id
        self.tmp2.created_at = self.tmp.created_at
        self.tmp2.updated_at = self.tmp.updated_at
        self.assertTrue(self.tmp == self.tmp2)

        self.tmp2.updated_at = datetime.now()
        self.assertFalse(self.tmp == self.tmp2)

        self.tmp2.__dict__ = self.tmp.__dict__
        self.assertTrue(self.tmp == self.tmp2)
