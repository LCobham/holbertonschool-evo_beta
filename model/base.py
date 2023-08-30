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
        obj_dict = self.__dict__
        obj_dict['__class__'] = type(self).__name__
        for attr in ('created_at', 'updated_at'):
            obj_dict[attr] = str(obj_dict.get(attr))
        return obj_dict

    @abstractclassmethod
    def constructor(cls, dictionary):
        pass

    def __eq__(self, obj):
        if type(obj) is type(self) and self.__dict__ == obj.__dict__:
            return True
        return False
    
    @property
    def dict_key(self):
        return f"{type(self).__name__}_{self.id}"
