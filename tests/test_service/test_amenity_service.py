#!/usr/bin/python3
"""
    Tests for the AmenityService Class
"""

from model.amenity import Amenity
from service.amenity_service import AmenityService
import unittest
from unittest.mock import patch
from model import storage
from persistance.file_storage import FileStorage
from datetime import datetime
import os


original_filename = storage._FileStorage__filename


class TestAmenityService(unittest.TestCase):
    """ Tests for the AmenityService Class """
    def setUp(self):
        if type(storage) is FileStorage:
            storage._FileStorage__filename = 'test_storage.json'
        storage.reload()

    def tearDown(self):
        if type(storage) is FileStorage:
            if os.access(storage._FileStorage__filename, os.F_OK):
                os.remove(storage._FileStorage__filename)
            storage._FileStorage__filename = original_filename

    def test_validate_name_unique(self):
        srvc = AmenityService
        wifi = Amenity(**{'name': 'WiFi'})

        mock_all_return = {wifi.key: wifi}

        # Mock the storage object so this test doesn't depend
        # on the success of another class
        with patch.object(storage, "all", return_value=mock_all_return) \
                as mock:
            # Test that no exception is raised with new name
            srvc.validate_name_is_unique('Garage')

            # Ensure the get method was called once
            mock.assert_called_once()

            with self.assertRaises(ValueError):
                srvc.validate_name_is_unique('WiFi')

    def test_create(self):
        am1 = {'name': 'WiFi'}

        # Test that no file exists previous to obj
        self.assertFalse(os.access(storage._FileStorage__filename, os.F_OK))

        wifi = AmenityService.create(**am1)
        # Test correct type

        self.assertTrue(type(wifi) is Amenity)

        # Test attrs are present & correct attribute types
        for key in am1:
            self.assertEqual(getattr(wifi, key), am1[key])
        self.assertTrue(type(wifi.id) is str)
        self.assertTrue(type(wifi.created_at) is datetime)
        self.assertTrue(type(wifi.updated_at) is datetime)

        # Test created_at == updated_at at creation
        self.assertEqual(wifi.created_at, wifi.updated_at)

        # Test that file is created -> obj is saved
        self.assertTrue(os.access(storage._FileStorage__filename, os.F_OK))

        storage.reload()
        self.assertEqual(len(storage.all('Amenity')), 1)
        self.assertEqual(storage.get(wifi.key), wifi)

        # Test everything still works with > 1 amenity
        am2 = {'name': 'Garage'}
        garage = AmenityService.create(**am2)

        storage.reload()
        self.assertEqual(len(storage.all('Amenity')), 2)
        self.assertIn(garage.key, storage.all('Amenity'))

        # Test create function fails if name is not unique

        with self.assertRaises(ValueError):
            AmenityService.create(**am1)

    def test_update(self):
        srvc = AmenityService
        am1 = {'name': 'wifi'}

        with self.assertRaises(KeyError):
            srvc.update('inexistent_id', **{'name': 'Garage'})

        wifi = srvc.create(**am1)

        # This is necessary because when updating, original objects are
        # modified so updated_at time would be updated on wifi object,
        # and not just in storage
        creation_updated_at = wifi.updated_at

        updated = srvc.update(wifi.id, **{'name': 'High Speed WiFi'})

        # Check that attributes have been correctly updated
        self.assertTrue(updated.updated_at > creation_updated_at)
        self.assertEqual(updated.name, 'High Speed WiFi')

        # Check that non-updated attributes hold their values
        for attr in ('id', 'created_at'):
            self.assertEqual(getattr(updated, attr), getattr(wifi, attr))

        # Check that updates are persisted
        storage.reload()
        storage_wifi = storage.get(wifi.key)

        self.assertEqual(storage_wifi.name, 'High Speed WiFi')
        # Note: in storage datetime objects are saved as str for serialization
        self.assertEqual(storage_wifi.updated_at, updated.updated_at)

    def test_delete(self):
        srvc = AmenityService
        am1 = {'name': 'WiFi'}
        wifi = srvc.create(**am1)

        srvc.delete(wifi.id)
        self.assertEqual(srvc.all(), {})

    def test_get(self):
        srvc = AmenityService
        am1 = {'name': 'WiFi'}
        wifi = srvc.create(**am1)

        storage_wifi = srvc.get(wifi.id)
        self.assertEqual(wifi, storage_wifi)

    def test_all(self):
        srvc = AmenityService
        am1 = {'name': 'WiFi'}
        wifi = srvc.create(**am1)

        all = srvc.all()
        self.assertEqual(type(all), dict)
        self.assertEqual(len(all), 1)
        self.assertEqual(all.get(wifi.key), wifi)

        am2 = {'name': 'Garage'}
        garage = srvc.create(**am2)

        all = srvc.all()
        self.assertEqual(len(all), 2)
        self.assertEqual(all.get(wifi.key), wifi)
        self.assertEqual(all.get(garage.key), garage)
