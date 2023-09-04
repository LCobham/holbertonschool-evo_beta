#!/usr/bin/python3
"""
    Tests for the UserService Class
"""

from model.user import User
from service.user_service import UserService, HASH_ITERATIONS
import unittest
from unittest.mock import patch
from model import storage
from persistance.file_storage import FileStorage
from datetime import datetime
from hashlib import pbkdf2_hmac
import os


original_filename = storage._FileStorage__filename


class TestUserService(unittest.TestCase):
    """ Tests for the UserService Class """
    def setUp(self):
        if type(storage) is FileStorage:
            storage._FileStorage__filename = 'test_storage.json'
        storage.reload()

    def tearDown(self):
        if type(storage) is FileStorage:
            if os.access(storage._FileStorage__filename, os.F_OK):
                os.remove(storage._FileStorage__filename)
            storage._FileStorage__filename = original_filename

    def test_validate_mail_is_unique(self):
        srvc = UserService

        usr1 = User("sfreud@gamil.com", "mom", "Sigmund", "Freud")
        mock_all_return = {usr1.key: usr1}

        # Mock the storage object so this test doesn't depend
        # on the success of another class
        with patch.object(storage, "all", return_value=mock_all_return) \
                as mock:

            # Test no exception is raised => mail is valid
            srvc.validate_mail_is_unique("johnstrand@yahoo.com")

            # Ensure the get method was called once
            mock.assert_called_once()

            # Test ValueError raised when mail is not unique
            with self.assertRaises(ValueError):
                srvc.validate_mail_is_unique(usr1.email)

    def test_create(self):
        srvc = UserService()
        u1 = {'email': 'bill@microsoft.com', 'password': 'Windows',
              'first_name': 'Bill', 'last_name': 'Gates'}

        # Test that no file exists previous to obj
        self.assertFalse(os.access(storage._FileStorage__filename, os.F_OK))
        bill = srvc.create(**u1)

        # Test correct type
        self.assertTrue(type(bill) is User)

        # Test attrs are present & correct attribute types
        for key in u1:
            if key != 'password':
                self.assertEqual(getattr(bill, key), u1[key])
            else:
                hash = pbkdf2_hmac(
                    'sha256', u1['password'].encode('utf-8'),
                    bill.id.encode('utf-8'), HASH_ITERATIONS
                )
                self.assertEqual(getattr(bill, key), hash.hex())

        self.assertTrue(type(bill.id) is str)
        self.assertTrue(type(bill.created_at) is datetime)
        self.assertTrue(type(bill.updated_at) is datetime)

        # Test created_at == updated_at at creation
        self.assertEqual(bill.created_at, bill.updated_at)

        # Test that file is created -> obj is saved
        self.assertTrue(os.access(storage._FileStorage__filename, os.F_OK))

        storage.reload()
        self.assertEqual(len(storage.all('User')), 1)
        self.assertEqual(storage.get(bill.key), bill)

        # Test everything still works with > 1 user
        u2 = {'email': 'mzuckerberg@fb.com', 'password': 'myspaceclone',
              'first_name': 'Mark', 'last_name': 'Zuckerberg'}
        mark = srvc.create(**u2)

        storage.reload()
        self.assertEqual(len(storage.all('User')), 2)
        self.assertIn(mark.key, storage.all('User'))

        # Test create function fails if mail is not unique
        u3 = {'email': 'mzuckerberg@fb.com', 'password': 'NewPswd',
              'first_name': 'Mark2', 'last_name': 'Zuckerberg2'}

        with self.assertRaises(ValueError):
            srvc.create(**u3)

    def test_update(self):
        srvc = UserService()
        u1 = {'email': 'bill@microsoft.com', 'password': 'Windows',
              'first_name': 'Bill', 'last_name': 'Gates'}

        with self.assertRaises(KeyError):
            srvc.update('inexistent_id', **{'password': '321456'})

        bill = srvc.create(**u1)

        # This is necessary because when updating, original objects
        # are modified so updated_at time would be updated on bill
        # object, and not just in storage
        creation_updated_at = bill.updated_at

        updated = srvc.update(bill.id, **{'first_name': 'William Henry'})

        # Check that attributes have been correctly updated
        self.assertTrue(updated.updated_at > creation_updated_at)
        self.assertEqual(updated.first_name, 'William Henry')

        # Check that non-updated attributes hold their values
        for attr in ('id', 'created_at', 'email', 'password', 'last_name'):
            self.assertEqual(getattr(updated, attr), getattr(bill, attr))

        # Check that updates are persisted
        storage.reload()
        storage_bill = storage.get(bill.key)

        self.assertEqual(storage_bill.first_name, 'William Henry')
        # Note: in storage, datetime objects are saved as str for serialization
        self.assertEqual(storage_bill.updated_at, updated.updated_at)

    def test_delete(self):
        srvc = UserService()
        u1 = {'email': 'bill@microsoft.com', 'password': 'Windows',
              'first_name': 'Bill', 'last_name': 'Gates'}
        bill = srvc.create(**u1)

        srvc.delete(bill.id)
        self.assertEqual(srvc.all(), {})

    def test_get(self):
        srvc = UserService()
        u1 = {'email': 'bill@microsoft.com', 'password': 'Windows',
              'first_name': 'Bill', 'last_name': 'Gates'}
        bill = srvc.create(**u1)

        storage_bill = srvc.get(bill.id)
        self.assertEqual(bill, storage_bill)

    def test_all(self):
        srvc = UserService()
        u1 = {'email': 'bill@microsoft.com', 'password': 'Windows',
              'first_name': 'Bill', 'last_name': 'Gates'}
        bill = srvc.create(**u1)

        all = srvc.all()
        self.assertEqual(type(all), dict)
        self.assertEqual(len(all), 1)
        self.assertEqual(all.get(bill.key), bill)

        u2 = {'email': 'mzuckerberg@fb.com', 'password': 'myspaceclone',
              'first_name': 'Mark', 'last_name': 'Zuckerberg'}
        mark = srvc.create(**u2)

        all = srvc.all()
        self.assertEqual(len(all), 2)
        self.assertEqual(all.get(bill.key), bill)
        self.assertEqual(all.get(mark.key), mark)
