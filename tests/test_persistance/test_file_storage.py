#!/usr/bin/python3
"""
    Tests for the FileStorage class
"""

from persistance.file_storage import FileStorage
from persistance.persistance import Persistance
from model.user import User
import unittest
import json
import os

filename = "test_storage.json"


class TestFileStorage(unittest.TestCase):
    """ Tests for FileStorage """

    def setUp(self):
        self.storage = FileStorage(filename)

    def tearDown(self):
        if os.access(filename, os.F_OK):
            os.remove(filename)

    def test_inheritance(self):
        self.assertTrue(isinstance(self.storage, Persistance))
        self.assertTrue(isinstance(self.storage, FileStorage))
        self.assertEqual(type(self.storage), FileStorage)

    def test_add(self):
        usr = User("john@mail.com", "123456", "John", "Doe")
        self.storage.add(usr)
        objects = self.storage.__dict__["_FileStorage__objects"]
        retrieved = objects.get(f"{type(usr).__name__}_{usr.id}")
        self.assertTrue(type(retrieved) is User)
        self.assertTrue(retrieved)
        self.assertEqual(retrieved.id, usr.id)

    def test_save(self):
        usr = User("john@mail.com", "123456", "John", "Doe")
        self.storage.add(usr)
        self.storage.save()

        # File with path=filename is created
        self.assertTrue(os.access(filename, os.F_OK))

        # Created file has correctly serialized object
        with open(filename, "r", encoding="utf-8") as f:
            loaded = json.load(f)

        retrieved = loaded.get(f"{type(usr).__name__}_{usr.id}")
        self.assertTrue(retrieved)
        self.assertEqual(retrieved, usr.to_dict())

    def test_reload(self):
        usr = User("john@mail.com", "123456", "John", "Doe")

        # Ensure file is created with serialized objects
        self.storage.add(usr)
        self.storage.save()

        # Delete objects currently in storage and verify deletion
        del self.storage._FileStorage__objects
        objects = self.storage.__dict__.get("_FileStorage__objects")
        self.assertFalse(objects)

        # Reload objects
        self.storage.reload()
        objects = self.storage.__dict__.get("_FileStorage__objects")

        # Verify obj types and info
        self.assertTrue(objects)
        retrieved = objects.get(f"{type(usr).__name__}_{usr.id}")
        self.assertTrue(retrieved)
        self.assertTrue(type(retrieved) is User)
        self.assertEqual(retrieved.id, usr.id)

    def test_remove(self):
        usr = User("john@mail.com", "123456", "John", "Doe")
        self.storage.add(usr)
        self.storage.remove(usr)

        objects = self.storage._FileStorage__objects
        # Verify that objects is empty
        self.assertEqual(objects, {})

    def test_get(self):
        usr = User("john@mail.com", "123456", "John", "Doe")
        self.storage.add(usr)
        retrieved = self.storage.get(usr.key)
        self.assertEqual(usr, retrieved)

    def test_all(self):
        usr = User("john@mail.com", "123456", "John", "Doe")
        self.storage.add(usr)

        all = self.storage.all()
        self.assertEqual(len(all), 1)
        self.assertEqual(all.get(usr.key), usr)

        new_user = User('janedoe@mail.com', '654321', 'Jane', 'Doe')
        self.storage.add(new_user)
        all = self.storage.all()
        self.assertEqual(len(all), 2)
        self.assertEqual(all.get(usr.key), usr)
        self.assertEqual(all, self.storage.all('User'))
