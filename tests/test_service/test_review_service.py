#!/usr/bin/python3
"""
    Tests for the ReviewService Class
"""

from model.review import Review
from service.review_service import ReviewService
from service.place_service import PlaceService
from service.user_service import UserService
from service.country_service import CountryService
from service.city_service import CityService
from service.amenity_service import AmenityService
import unittest
from unittest.mock import patch
from model import storage
from persistance.file_storage import FileStorage
from datetime import datetime
import os


original_filename = storage._FileStorage__filename


class TestReviewService(unittest.TestCase):
    """ Tests for the ReviewService Class """
    def setUp(self):
        if type(storage) is FileStorage:
            storage._FileStorage__filename = 'test_storage.json'
        storage.reload()

        self.user = UserService.create(**{
            'email': 'jdoe@test.com',
            'password': '123456',
            'first_name': 'John',
            'last_name': 'Doe'
        })

        self.country = CountryService.create(**{
            'name': 'Uruguay',
            'iso': 'UY'
        })

        self.city = CityService.create(**{
            'name': 'Carmelo',
            'country': self.country.id
        })

        self.wifi = AmenityService.create(**{
            'name': 'WiFi'
        })

        self.garage = AmenityService.create(**{
            'name': 'Garage'
        })

        data = {
            'name': 'Travellers Inn',
            'description': 'Lovely atmosphere &'
            'close to the city center',
            'address': '18 de Julio 2233',
            'host': self.user.id,
            'latitude': 37.2456,
            'longitude': 33.4455,
            'city': self.city.id,
            'country': self.country.id,
            'price_per_night': 130,
            'max_guests': 6,
            'number_rooms': 3,
            'number_bathrooms': 2,
            'amenities': [self.wifi.id, self.garage.id]
        }

        self.place = PlaceService.create(**data)
        storage.reload()

    def tearDown(self):
        if type(storage) is FileStorage:
            if os.access(storage._FileStorage__filename, os.F_OK):
                os.remove(storage._FileStorage__filename)
            storage._FileStorage__filename = original_filename

    def test_user_is_valid(self):
        # Test raises exception on wrong user ID
        with self.assertRaises(ValueError):
            ReviewService.user_is_valid('wrong_id')

        # Test raises error on non-user ID
        with self.assertRaises(ValueError):
            ReviewService.user_is_valid(self.country.id)

        # No exception on correct user ID
        ReviewService.user_is_valid(self.user.id)

    def test_place_is_valid(self):
        # Test raises exception on wrong user ID
        with self.assertRaises(ValueError):
            ReviewService.place_is_valid('wrong_id')

        # Test raises error on non-user ID
        with self.assertRaises(ValueError):
            ReviewService.place_is_valid(self.country.id)

        # No exception on correct user ID
        ReviewService.place_is_valid(self.place.id)

    def test_create(self):
        # Test that place.reviews is empty before creating Review
        self.assertEqual(self.place.reviews, [])

        gordon = UserService.create(**{
            'email': 'gramsey@gmail.com',
            'password': 'xdxdxd',
            'first_name': 'Gordon',
            'last_name': 'Ramsey'
        })

        data = {
            'place': self.place.id,
            'user': gordon.id,
            'rating': 7,
            'comment':
            "Amazing palce but the hotel restaurant was bad"
        }

        review = ReviewService.create(**data)

        # Test correct type
        self.assertTrue(type(review) is Review)

        # Test attrs are present & correct attribute types
        for key in data:
            self.assertEqual(getattr(review, key), data[key])
        self.assertTrue(type(review.id) is str)
        self.assertTrue(type(review.created_at) is datetime)
        self.assertTrue(type(review.updated_at) is datetime)

        # Test created_at == updated_at at creation
        self.assertEqual(review.created_at, review.updated_at)

        storage.reload()
        self.assertEqual(len(storage.all('Review')), 1)
        self.assertEqual(storage.get(review.key), review)

        # Test that place.reviews is correctly updated
        self.assertEqual(PlaceService.get(self.place.id).reviews, [review.id])

    def test_update(self):
        with self.assertRaises(KeyError):
            ReviewService.update('inexistent_id', **{'rating': 2})

        gordon = UserService.create(**{
            'email': 'gramsey@gmail.com',
            'password': 'xdxdxd',
            'first_name': 'Gordon',
            'last_name': 'Ramsey'
        })

        data = {
            'place': self.place.id,
            'user': gordon.id,
            'rating': 7,
            'comment':
            "Amazing palce but the hotel restaurant was bad"
        }

        review = ReviewService.create(**data)

        updated = ReviewService.update(review.id, **{'rating': 2})

        # Check that attributes have been correctly updated
        self.assertTrue(updated.updated_at > updated.created_at)
        self.assertEqual(updated.rating, 2)

        # Check that non-updated attributes hold their values
        for attr in ('id', 'created_at', 'user', 'place', 'comment'):
            self.assertEqual(getattr(updated, attr), getattr(review, attr))

        # Check that updates are persisted
        storage.reload()
        storage_review = storage.get(review.key)

        self.assertEqual(storage_review.rating, 2)
        # Note: in storage, datetime objects are saved as str for serialization
        self.assertEqual(storage_review.updated_at, updated.updated_at)

    def test_delete(self):
        gordon = UserService.create(**{
            'email': 'gramsey@gmail.com',
            'password': 'xdxdxd',
            'first_name': 'Gordon',
            'last_name': 'Ramsey'
        })

        data = {
            'place': self.place.id,
            'user': gordon.id,
            'rating': 7,
            'comment':
            "Amazing palce but the hotel restaurant was bad"
        }

        review = ReviewService.create(**data)

        ReviewService.delete(review.id)
        self.assertEqual(ReviewService.all(), {})

    def test_get(self):
        gordon = UserService.create(**{
            'email': 'gramsey@gmail.com',
            'password': 'xdxdxd',
            'first_name': 'Gordon',
            'last_name': 'Ramsey'
        })

        data = {
            'place': self.place.id,
            'user': gordon.id,
            'rating': 7,
            'comment':
            "Amazing palce but the hotel restaurant was bad"
        }

        review = ReviewService.create(**data)

        storage_review = ReviewService.get(review.id)
        self.assertEqual(review, storage_review)

    def test_all(self):
        gordon = UserService.create(**{
            'email': 'gramsey@gmail.com',
            'password': 'xdxdxd',
            'first_name': 'Gordon',
            'last_name': 'Ramsey'
        })

        data = {
            'place': self.place.id,
            'user': gordon.id,
            'rating': 7,
            'comment':
            "Amazing palce but the hotel restaurant was bad"
        }

        review = ReviewService.create(**data)

        all = ReviewService.all()
        self.assertEqual(len(all), 1)
        self.assertEqual(all.get(review.key), review)
