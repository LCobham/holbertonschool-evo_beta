#!/usr/bin/python3
"""
    Tests for the CityService Class
"""

from model.city import City
from service.city_service import CityService
from service.country_service import CountryService
import unittest
from unittest.mock import patch
from model import storage
from persistance.file_storage import FileStorage
from datetime import datetime
import os


original_filename = storage._FileStorage__filename


class TestCityService(unittest.TestCase):
    """ Tests for the CityService Class """
    def setUp(self):
        if type(storage) is FileStorage:
            storage._FileStorage__filename = 'test_storage.json'
        storage.reload()
        uru = {'name': 'Uruguay', 'iso': 'UY'}
        self.uruguay = CountryService.create(**uru)

    def tearDown(self):
        if type(storage) is FileStorage:
            if os.access(storage._FileStorage__filename, os.F_OK):
                os.remove(storage._FileStorage__filename)
            storage._FileStorage__filename = original_filename

    def test_country_is_valid(self):
        srvc = CityService

        mock_get_return = None

        # Mock the storage object so this test doesn't depend
        # on the success of another class
        with patch.object(storage, "get", return_value=mock_get_return) \
                as mock:
            with self.assertRaises(ValueError):
                srvc.country_is_valid('inexistent country id')

            mock.assert_called_once()

        mock_get_return = self.uruguay

        with patch.object(storage, "get", return_value=mock_get_return) \
                as mock:
            srvc.country_is_valid(self.uruguay.id)

    def test_create(self):
        srvc = CityService

        # Test that country.cities is empty before creating city
        self.assertEqual(self.uruguay.cities, [])

        data = {'name': 'Montevideo', 'country': self.uruguay.id}
        city = srvc.create(**data)

        # Test correct type
        self.assertTrue(type(city) is City)

        # Test attrs are present & correct attribute types
        for key in data:
            self.assertEqual(getattr(city, key), data[key])
        self.assertTrue(type(city.id) is str)
        self.assertTrue(type(city.created_at) is datetime)
        self.assertTrue(type(city.updated_at) is datetime)

        # Test created_at == updated_at at creation
        self.assertEqual(city.created_at, city.updated_at)

        storage.reload()
        self.assertEqual(len(storage.all('City')), 1)
        self.assertEqual(storage.get(city.key), city)

        # Test that country.cities is correctly updated
        self.assertEqual(CountryService.get(self.uruguay.id).cities, [city.id])

        # Test everything still works with > 1 City
        data2 = {'name': 'Punta del Este', 'country': self.uruguay.id}
        city2 = CityService.create(**data2)

        self.assertEqual(len(CountryService.get(self.uruguay.id).cities), 2)

        storage.reload()
        self.assertEqual(len(storage.all('City')), 2)
        self.assertIn(city2.key, storage.all('City'))

    def test_update(self):
        srvc = CityService

        with self.assertRaises(KeyError):
            srvc.update('inexistent_id', **{'name': 'Buenos Aires'})

        data = {'name': 'Montevideo', 'country': self.uruguay.id}
        city = srvc.create(**data)

        # This is necessary because when updating, original objects
        # are modified so updated_at time would be updated on city
        # object, and not just in storage
        creation_updated_at = city.updated_at

        updated = srvc.update(city.id, **{'name': 'Colonia'})

        # Check that attributes have been correctly updated
        self.assertTrue(updated.updated_at > creation_updated_at)
        self.assertEqual(updated.name, 'Colonia')

        # Check that non-updated attributes hold their values
        for attr in ('id', 'created_at', 'country'):
            self.assertEqual(getattr(updated, attr), getattr(city, attr))

        # Check that updates are persisted
        storage.reload()
        storage_city = storage.get(city.key)

        self.assertEqual(storage_city.name, 'Colonia')
        # Note: in storage, datetime objects are saved as str for serialization
        self.assertEqual(storage_city.updated_at, updated.updated_at)

    def test_delete(self):
        srvc = CityService
        data = {'name': 'Montevideo', 'country': self.uruguay.id}
        city = srvc.create(**data)

        srvc.delete(city.id)
        self.assertEqual(srvc.all(), {})

    def test_get(self):
        srvc = CityService
        data = {'name': 'Montevideo', 'country': self.uruguay.id}
        city = srvc.create(**data)

        storage_city = srvc.get(city.id)
        self.assertEqual(city, storage_city)

    def test_all(self):
        srvc = CityService
        data = {'name': 'Montevideo', 'country': self.uruguay.id}
        city = srvc.create(**data)

        all = srvc.all()
        self.assertEqual(type(all), dict)
        self.assertEqual(len(all), 1)
        self.assertEqual(all.get(city.key), city)

        data2 = {'name': 'Punta del Este', 'country': self.uruguay.id}
        city2 = CityService.create(**data2)

        all = srvc.all()
        self.assertEqual(len(all), 2)
        self.assertEqual(all.get(city.key), city)
        self.assertEqual(all.get(city2.key), city2)
