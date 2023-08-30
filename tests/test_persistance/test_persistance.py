#!/usr/bin/python3
"""
    This module tests the Persistance Abstract class.
"""

from persistance.persistance import Persistance
import unittest


class TestPersistance(unittest.TestCase):
    """ Test the Persistance Abstract Class """

    def setUp(self):
        class TestPersistance(Persistance):
            __objects = {}

            def save(self):
                pass

            def add(self, obj):
                self.__objects[f"{type(obj).__name}_{obj.id}"] = obj

            def remove(self, obj):
                if self.__objects.get(f"{type(obj).__name}_{obj.id}"):
                    del self.__objects[f"{type(obj).__name}_{obj.id}"]

            def reload(self):
                pass

            def get(self, classname, id):
                return self.__objects.get(f"{str(classname)}_{id}")

            def all(self, classname=None):
                if classname:
                    return dict(filter(
                        self.__objects.items(),
                        key=lambda x: x[1]['__class__'] == classname))

                return self.__objects

        self.test = TestPersistance()

    def test_cant_instantiate_base(self):
        with self.assertRaises(TypeError):
            Persistance()
