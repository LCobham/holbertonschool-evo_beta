#!/usr/bin/python3
"""
    This module defines an interface for Persistance classes
    (FileStorage and DataBaseStorage).
"""

from abc import ABC, abstractmethod


class Persistance(ABC):
    """
    Interface for classes that handle the persistance of Objects.
    """

    @abstractmethod
    def add(self, obj):
        """ Adds an object from the storage. Changes aren't committed """
        pass

    @abstractmethod
    def save(self):
        """ Commits the changes """
        pass

    @abstractmethod
    def remove(self, obj):
        """ Removes an object from the storage. Changes aren't committed """
        pass

    @abstractmethod
    def reload(self):
        """ Reloads all previously saved objects """
        pass

    @abstractmethod
    def get(self, cls, id):
        """ Get a specific item by ID """
        pass

    @abstractmethod
    def all(self, cls):
        """ Get all objects or all objects of a given class in storage """
        pass
