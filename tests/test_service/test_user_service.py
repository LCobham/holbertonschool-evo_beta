#!/usr/bin/python3
"""
    Tests for the UserService Class
"""

from model.user import User
from service.user_service import UserService
import unittest
from unittest.mock import patch
from model import storage
from persistance.file_storage import FileStorage
from datetime import datetime
import os
import json


original_filename = storage._FileStorage__filename


class TestUserService(unittest.TestCase):
    """ Tests for the UserService Class """
    def setUp(self):
        if type(storage) is FileStorage:
            storage._FileStorage__filename = 'test_storage.json'

    def tearDown(self):
        if type(storage) is FileStorage:
            if os.access(storage._FileStorage__filename, os.F_OK):
                os.remove(storage._FileStorage__filename)
            storage._FileStorage__filename = original_filename

    def test_validate_mail_is_unique(self):
        srvc = UserService()

        usr1 = User("sfreud@gamil.com", "mom", "Sigmund", "Freud")
        mock_get_return = {f"User_{usr1.id}": usr1}

        # Mock the storage object so this test doesn't depend
        # on the success of another class       
        with patch.object(storage, "all", return_value=mock_get_return) as mock:
            self.assertTrue(srvc.validate_mail_is_unique("johnstrand@yahoo.com"))

            # Ensure the get method was called once
            mock.assert_called_once()

            self.assertFalse(srvc.validate_mail_is_unique(usr1.email))

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
            self.assertEqual(getattr(bill, key), u1[key])
        self.assertTrue(type(bill.id) is str)
        self.assertTrue(type(bill.created_at) is datetime)
        self.assertTrue(type(bill.updated_at) is datetime)

        # Test created_at == updated_at at creation
        self.assertEqual(bill.created_at, bill.updated_at)

        # Test that file is created -> obj is saved
        self.assertTrue(os.access(storage._FileStorage__filename, os.F_OK))

        with open(storage._FileStorage__filename, "r", encoding="utf-8") as f:
            persistence = json.load(f)

        self.assertTrue(type(persistence) is dict)
        self.assertEqual(len(persistence.values()), 1)
        self.assertTrue(persistence.get(bill.key))
        self.assertEqual(persistence.get(bill.key)['id'], bill.id)

        # Test everything still works with > 1 user
        u2 = {'email': 'mzuckerberg@fb.com', 'password': 'myspaceclone',
              'first_name': 'Mark', 'last_name': 'Zuckerberg'}
        mark = srvc.create(**u2)

        with open(storage._FileStorage__filename, "r", encoding="utf-8") as f:
            persistence = json.load(f)

        self.assertEqual(len(persistence.values()), 2)
        self.assertEqual(persistence.get(mark.key)['id'], mark.id)

    def test_update(self):
        pass
