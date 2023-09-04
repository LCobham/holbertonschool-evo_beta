#!/usr/bin/python3
"""
    Tests for the PlaceService Class
"""

import unittest
import os
from datetime import datetime
from model import storage
from persistance.file_storage import FileStorage
from model.place import Place
from service.place_service import PlaceService
from service.amenity_service import AmenityService
from service.city_service import CityService
from service.country_service import CountryService
from service.user_service import UserService


original_filename = storage._FileStorage__filename


class TestPlaceService(unittest.TestCase):
    """ Tests for the PlaceService Class """
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

    def tearDown(self):
        if type(storage) is FileStorage:
            if os.access(storage._FileStorage__filename, os.F_OK):
                os.remove(storage._FileStorage__filename)
            storage._FileStorage__filename = original_filename

    def test_host_is_valid(self):
        # Test raises error on non-existent User ID
        with self.assertRaises(ValueError):
            PlaceService.host_is_valid('inexistent_uid')

        # Test raises error on ID of non-user object
        with self.assertRaises(ValueError):
            PlaceService.host_is_valid(self.country.id)

        # No exception is raised on valid User ID
        PlaceService.host_is_valid(self.user.id)

    def test_city_is_valid(self):
        # Test raises error on non-existent User ID
        with self.assertRaises(ValueError):
            PlaceService.city_is_valid('inexistent_uid')

        # Test raises error on ID of non-city object
        with self.assertRaises(ValueError):
            PlaceService.city_is_valid(self.country.id)

        # No exception is raised on valid City ID
        PlaceService.city_is_valid(self.city.id)

    def test_amenities_are_valid(self):
        # Test raises error if one amenity doesn't exists
        with self.assertRaises(ValueError):
            PlaceService.amenities_are_valid([
                self.wifi.id, self.garage.id, 'wrong'
            ])

        with self.assertRaises(ValueError):
            PlaceService.amenities_are_valid([
                self.wifi.id, 'wrong', self.garage.id
            ])

        with self.assertRaises(ValueError):
            PlaceService.amenities_are_valid([
                'wrong', self.wifi.id, self.garage.id
            ])

        # No exception raised with existing amenities
        PlaceService.amenities_are_valid([
            self.wifi.id, self.garage.id
        ])

    def test_reviews_are_valid(self):
        from service.review_service import ReviewService

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

        place = PlaceService.create(**data)

        rev = {
            'user': self.user.id,
            'place': place.id,
            'rating': 4,
            'comment': 'Not clean'
        }
        review = ReviewService.create(**rev)

        # Test exceptions
        with self.assertRaises(TypeError):
            PlaceService.reviews_are_valid(review.id)

        with self.assertRaises(ValueError):
            PlaceService.reviews_are_valid(['inexistent_uid'])

        with self.assertRaises(ValueError):
            PlaceService.reviews_are_valid([review.id, 'inexistent_uid'])

        # No exception is raised on correct input
        PlaceService.reviews_are_valid([review.id])

    def test_create(self):
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

        place = PlaceService.create(**data)

        # Test correct type
        self.assertTrue(type(place) is Place)

        # Test attrs are present & correct attribute types
        for key in data:
            self.assertEqual(getattr(place, key), data[key])
        self.assertTrue(type(place.id) is str)
        self.assertTrue(type(place.created_at) is datetime)
        self.assertTrue(type(place.updated_at) is datetime)

        # Test create fails on wrong input
        with self.assertRaises(TypeError):
            cpy = data.copy()
            cpy['name'] = 321
            PlaceService.create(**cpy)

        with self.assertRaises(TypeError):
            cpy = data.copy()
            cpy['description'] = 321
            PlaceService.create(**cpy)

        with self.assertRaises(TypeError):
            cpy = data.copy()
            cpy['address'] = 321
            PlaceService.create(**cpy)

        with self.assertRaises(TypeError):
            cpy = data.copy()
            cpy['latitude'] = 'str'
            PlaceService.create(**cpy)

        with self.assertRaises(TypeError):
            cpy = data.copy()
            cpy['longitude'] = 'str'
            PlaceService.create(**cpy)

        with self.assertRaises(TypeError):
            cpy = data.copy()
            cpy['latitude'] = 'str'
            PlaceService.create(**cpy)

        with self.assertRaises(TypeError):
            cpy = data.copy()
            cpy['price_per_night'] = '99'
            PlaceService.create(**cpy)

        with self.assertRaises(TypeError):
            cpy = data.copy()
            cpy['max_guests'] = '12'
            PlaceService.create(**cpy)

        with self.assertRaises(TypeError):
            cpy = data.copy()
            cpy['number_rooms'] = '2'
            PlaceService.create(**cpy)

        with self.assertRaises(TypeError):
            cpy = data.copy()
            cpy['number_bathrooms'] = 2.5
            PlaceService.create(**cpy)

        # Test create fails when validations fail
        with self.assertRaises(ValueError):
            cpy = data.copy()
            cpy['host'] = 'wrong_id'
            PlaceService.create(**cpy)

        with self.assertRaises(ValueError):
            cpy = data.copy()
            cpy['city'] = 'wrong_id'
            PlaceService.create(**cpy)

        with self.assertRaises(ValueError):
            cpy = data.copy()
            cpy['country'] = 'wrong_id'
            PlaceService.create(**cpy)

        # Test created_at == updated_at at creation
        self.assertEqual(place.created_at, place.updated_at)

        # Test object is correclt persisted
        storage.reload()
        self.assertEqual(len(storage.all('Place')), 1)
        self.assertEqual(storage.get(place.key), place)

    def test_update(self):
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

        place = PlaceService.create(**data)

        with self.assertRaises(KeyError):
            PlaceService.update('wrong', **{'name': 'Hello'})

        updated = PlaceService.update(place.id, **{
            'name': "The Best Traveller's Inn"
            })

        required = (
            'description', 'address', 'city', 'country',
            'latitude', 'longitude', 'host', 'price_per_night',
            'max_guests', 'number_rooms', 'number_bathrooms',
            'amenities', 'reviews', 'created_at', 'id'
        )

        for attr in required:
            self.assertEqual(getattr(place, attr), getattr(updated, attr))

        self.assertTrue(updated.updated_at > place.created_at)
        storage.reload()
        storage_place = storage.get(place.key)

        self.assertEqual(storage_place.name, "The Best Traveller's Inn")

    def test_delete(self):
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

        place = PlaceService.create(**data)
        self.assertTrue(PlaceService.all())

        PlaceService.delete(place.id)
        self.assertEqual(PlaceService.all(), {})

    def test_get(self):
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

        place = PlaceService.create(**data)

        retrieved = PlaceService.get(place.id)
        self.assertEqual(place, retrieved)

    def test_all(self):
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

        place = PlaceService.create(**data)

        all = PlaceService.all()
        self.assertEqual(type(all), dict)
        self.assertEqual(len(all), 1)
