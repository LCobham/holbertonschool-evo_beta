#!/usr/bin/python3
"""
    This module defines the FileStorage class for persisting
    objects to a file in JSON format.
"""
import json
import os
import sys
from persistance.persistance import Persistance
from model.base import BaseModel


class FileStorage(Persistance):
    """
        FileStorage class for persisting AirBnB objects
        in a file.
    """

    def __init__(self, filename):
        if not filename:
            raise AttributeError('filename missing')
        if type(filename) is not str:
            raise TypeError('filename must be string')
        self.__filename = filename

        if os.access(filename, os.R_OK):
            self.reload()
        else:
            self.__objects = {}

    def reload(self):
        """ Reload all objects into the self.__objects field """
        from model import classes
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                reload = json.load(f)

            self.__objects = {}
            for key, value in reload.items():
                obj_cls = classes[value['__class__']]
                self.__objects[key] = obj_cls.constructor(value)

        except FileNotFoundError:
            sys.stderr.write("File path was not found")

    def add(self, object):
        """ Adds an element to storage without committing changes """
        if not isinstance(object, BaseModel):
            raise TypeError("trying to add to storage an object"
                            " that's not derived from BaseModel")
        self.__objects[f"{type(object).__name__}_{object.id}"] = object

    def save(self):
        """ Saves uncommitted changes """
        try:
            # Verify there are objects to save. If an empty file is created
            # this will raise an error when we try to reload the objects.
            if self.__objects:
                obj_dict = {}
                for key, value in self.__objects.items():
                    obj_dict[key] = value.to_dict()

                with open(self.__filename, "w", encoding="utf-8") as f:
                    json.dump(obj_dict, f, indent=2)

        except Exception:
            sys.stderr.write("Couldn't write to file")

    def remove(self, object):
        """ Removes an object from storage if found. Doesn't save changes """
        if self.__objects.get(f"{type(object).__name__}_{object.id}"):
            del self.__objects[f"{type(object).__name__}_{object.id}"]

    def get(self, key):
        """ Get a specific element from storage """
        return self.__objects.get(key)

    def all(self, classname=None):
        """ Returns all elements of a specific class in storage """
        if not classname:
            return self.__objects

        return dict(
                filter(
                    lambda x: type(x[1]).__name__ == classname,
                    self.__objects.items())
                )
