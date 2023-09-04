#!/usr/bin/python3
"""
    Tests for the CountryService Class
"""

from model.country import Country
from service.country_service import CountryService
import unittest
# from unittest.mock import patch # Not neccessary if no validation
from model import storage
from persistance.file_storage import FileStorage
from datetime import datetime
import os


original_filename = storage._FileStorage__filename


class TestCountryService(unittest.TestCase):
    """ Tests for the CountryService Class """
    def setUp(self):
        if type(storage) is FileStorage:
            storage._FileStorage__filename = 'test_storage.json'
        storage.reload()

    def tearDown(self):
        if type(storage) is FileStorage:
            if os.access(storage._FileStorage__filename, os.F_OK):
                os.remove(storage._FileStorage__filename)
            storage._FileStorage__filename = original_filename

    def test_create(self):
        data = {'name': 'Uruguay', 'iso': 'UY'}

        # Test that no file exists previous to obj
        self.assertFalse(os.access(storage._FileStorage__filename, os.F_OK))

        uru = CountryService.create(**data)

        # Test correct type
        self.assertTrue(type(uru) is Country)

        # Test attrs are present & correct attribute types
        for key in data:
            self.assertEqual(getattr(uru, key), data[key])
        self.assertTrue(type(uru.id) is str)
        self.assertTrue(type(uru.created_at) is datetime)
        self.assertTrue(type(uru.updated_at) is datetime)

        # Test created_at == updated_at at creation
        self.assertEqual(uru.created_at, uru.updated_at)

        # Test that file is created -> obj is saved
        self.assertTrue(os.access(storage._FileStorage__filename, os.F_OK))

        storage.reload()
        self.assertEqual(len(storage.all('Country')), 1)
        self.assertEqual(storage.get(uru.key), uru)

        # Test everything still works with > 1 Country
        data2 = {'name': 'Argentina', 'iso': 'AR'}
        arg = CountryService.create(**data2)

        storage.reload()
        self.assertEqual(len(storage.all('Country')), 2)
        self.assertIn(arg.key, storage.all('Country'))

    def test_update(self):
        srvc = CountryService
        data = {'name': 'Uruguay', 'iso': 'UR'}

        with self.assertRaises(KeyError):
            srvc.update('inexistent_id', **data)

        uru = srvc.create(**data)

        # This is necessary because when updating, original objects
        # are modified so updated_at time would be updated on uru
        # object, and not just in storage
        creation_updated_at = uru.updated_at

        updated = srvc.update(uru.id, **{'iso': 'UY'})

        # Check that attributes have been correctly updated
        self.assertTrue(updated.updated_at > creation_updated_at)
        self.assertEqual(updated.iso, 'UY')

        # Check that non-updated attributes hold their values
        for attr in ('id', 'created_at', 'name'):
            self.assertEqual(getattr(updated, attr), getattr(uru, attr))

        # Check that updates are persisted
        storage.reload()
        storage_uru = storage.get(uru.key)

        self.assertEqual(storage_uru.iso, 'UY')
        # Note: in storage, datetime objects are saved as str for serialization
        self.assertEqual(storage_uru.updated_at, updated.updated_at)

    def test_delete(self):
        srvc = CountryService
        data = {'name': 'Uruguay', 'iso': 'UR'}
        uru = srvc.create(**data)

        srvc.delete(uru.id)
        self.assertEqual(srvc.all(), {})

    def test_get(self):
        srvc = CountryService
        data = {'name': 'Uruguay', 'iso': 'UR'}
        uru = srvc.create(**data)

        storage_uru = srvc.get(uru.id)
        self.assertEqual(uru, storage_uru)

    def test_all(self):
        srvc = CountryService
        data = {'name': 'Uruguay', 'iso': 'UR'}
        uru = srvc.create(**data)

        all = srvc.all()
        self.assertEqual(type(all), dict)
        self.assertEqual(len(all), 1)
        self.assertEqual(all.get(uru.key), uru)

        data2 = {'name': 'Argentina', 'iso': 'AR'}
        arg = CountryService.create(**data2)

        all = srvc.all()
        self.assertEqual(len(all), 2)
        self.assertEqual(all.get(uru.key), uru)
        self.assertEqual(all.get(arg.key), arg)
