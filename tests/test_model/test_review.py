#!/usr/bin/python3
"""
    Tests for Review class
"""

import unittest
from model.review import Review
from model.place import Place
from model.amenity import Amenity
from model.user import User
from model.country import Country
from model.city import City
from model.base import BaseModel


class TestReview(unittest.TestCase):
    """ Tests for the Review class """

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

        place = Place(**inputs)
        mike = User("mike_brown@test.com", "12341234", "Mike", "B")

        self.review = Review(mike.key, place.key, 7, 'Nice, nice.')

    def test_inheritance(self):
        self.assertIsInstance(self.review, BaseModel)
        self.assertIsInstance(self.review, Review)
        self.assertEqual(type(self.review), Review)

    def test_attrs(self):
        review = self.review
        self.assertTrue(hasattr(review, 'id'))
        self.assertTrue(hasattr(review, 'created_at'))
        self.assertTrue(hasattr(review, 'updated_at'))

        atributes = (
            'user', 'place', 'rating', 'comment'
        )
        for atr in atributes:
            self.assertTrue(hasattr(review, atr))

    def test_mandatory_fields(self):
        with self.assertRaises(TypeError):
            Review()

    def test_setters(self):
        with self.assertRaises(TypeError):
            self.review.user = 22

        with self.assertRaises(TypeError):
            self.review.place = (1, 2, 3)

        with self.assertRaises(TypeError):
            self.review.rating = 3.14

        with self.assertRaises(TypeError):
            self.review.comment = 35

    def test_inherited_methods(self):
        review = self.review
        review_dict = review.to_dict()
        self.assertEqual(review_dict.get('__class__'), type(review).__name__)
        self.assertEqual(review_dict.get('id'), review.id)

    def test_review_constructor(self):
        review = self.review
        new = Review.constructor(review.to_dict())
        self.assertEqual(review, new)
