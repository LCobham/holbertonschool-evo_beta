#!/usr/bin/python3
"""
    Tests for User class
"""

import unittest
from model.user import User
from model.base import BaseModel


class TestUser(unittest.TestCase):
    """ Test class for User """

    def setUp(self):
        self.user = User('jdoe@mail.com', 'password', 'John', 'Doe')

    def test_inheritance(self):
        self.assertIsInstance(self.user, BaseModel)
        self.assertIsInstance(self.user, User)
        self.assertEqual(type(self.user), User)

    def test_attrs(self):
        usr = self.user
        self.assertTrue(hasattr(usr, 'id'))
        self.assertTrue(hasattr(usr, 'created_at'))
        self.assertTrue(hasattr(usr, 'updated_at'))
        self.assertTrue(hasattr(usr, 'email'))
        self.assertTrue(hasattr(usr, 'password'))
        self.assertTrue(hasattr(usr, 'first_name'))
        self.assertTrue(hasattr(usr, 'last_name'))

    def test_mandatory_fields(self):
        with self.assertRaises(TypeError):
            user = User()

        with self.assertRaises(TypeError):
            user = User('jdoe@mail.com')

        with self.assertRaises(TypeError):
            user = User(password='password')


    def test_setters(self):
        with self.assertRaises(TypeError):
            self.user.first_name = 22

        with self.assertRaises(TypeError):
            self.user.last_name = (1, 2, 3)
        
        with self.assertRaises(TypeError):
            self.user.email = 3.14

        with self.assertRaises(TypeError):
            self.user.password = 35

    def test_inherited_methods(self):
        usr = self.user
        usr_dict = usr.to_dict()
        self.assertEqual(usr_dict.get('__class__'), type(usr).__name__)
        self.assertEqual(usr_dict.get('id'), usr.id)
        self.assertEqual(usr_dict.get('email'), usr.email)
        self.assertEqual(usr_dict.get('first_name'), usr.first_name)

    def test_user_constructor(self):
        usr = self.user
        new = User.constructor(usr.to_dict())
        self.assertEqual(usr, new)
