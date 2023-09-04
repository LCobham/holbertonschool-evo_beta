#!/usr/bin/python3
"""
    This module defines the Abstract Class that will
    serve as the Base for all model classes of the
    AirBnB Clone
"""

from abc import ABC, abstractclassmethod
from datetime import datetime
from uuid import uuid4


class BaseModel(ABC):
    """
    Abstract class for all model classes.
    Attrs:
        - id: string (UUID4)
        - created_at: datetime
        - updated_at: datetime

    Methods:
        - to_dict: Returns a dictionary representation of the object
        with an attribute to indicate the class of the object

        - constructor: Build an instance of an object from a dictionary.
        User for deserialization
    """

    def __init__(self):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def to_dict(self):
        """
            Returns an object's dictionary representation for serialization.
            Datetime objects are converted to string and an attribute is added
            to store the object's type
        """

        # Need to parse keys since private attrs generate name mangling
        obj_dict = {
            key.replace(f'_{type(self).__name__}__', ''): self.__dict__[key]
            for key in self.__dict__
        }

        obj_dict['__class__'] = type(self).__name__
        for attr in ('created_at', 'updated_at'):
            obj_dict[attr] = str(obj_dict.get(attr))
        return obj_dict

    @classmethod
    def constructor(cls, dictionary):
        required = cls.required()

        if 'id' not in dictionary:
            raise KeyError('id not in dictionary')
        if type(dictionary.get('id')) is not str:
            raise TypeError('id must be a string')

        if 'created_at' not in dictionary:
            raise KeyError('created_at not in dictionary')
        if type(dictionary.get('created_at')) is not str:
            raise TypeError('created_at must be a string')

        if 'updated_at' not in dictionary:
            raise KeyError('updated_at not in dictionary')
        if type(dictionary.get('created_at')) is not str:
            raise TypeError('created_at must be a string')

        required_inputs = {
            key: dictionary.get(key)
            for key in required
        }

        created_at = datetime.fromisoformat(dictionary['created_at'])
        updated_at = datetime.fromisoformat(dictionary['updated_at'])

        new_instance = cls(**required_inputs)

        new_instance.id = dictionary.get('id')
        new_instance.created_at = created_at
        new_instance.updated_at = updated_at
        return new_instance

    def __eq__(self, obj):
        if type(obj) is type(self) and self.__dict__ == obj.__dict__:
            return True
        return False

    @classmethod
    def required(cls):
        return cls.__dict__[f"_{cls.__name__}__required"]

    @property
    def key(self):
        return f"{type(self).__name__}_{self.id}"
