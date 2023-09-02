#!/usr/bin/python3
"""
    This module creates an interface for the
    Services Classes in the AirBnB project
"""

from abc import ABC
from model import storage
from datetime import datetime


class ServiceBase(ABC):
    """
        Interface for the Services Classes
        Class Attrs:
            - __service_class: class to which the service is provided
            (ex: UserService -> __service_class = User)
        Methods:
            - create: Handles Business logic for creating objects
            - get: Gets an item from the storage with a given key
            - update: Updates the fields of an object in storage
            - delete: Deletes an item from the storage
    """
    __service_class = None

    def create(self, **inputs):
        service_cls = type(self).service_class()
        required_inputs = service_cls.required()

        # Get only relevant information
        subset = {key: inputs[key] for key in required_inputs}

        new_instance = service_cls(**subset)
        storage.add(new_instance)
        storage.save()

        return new_instance

    def update(self, id, **inputs):
        srvc_cls = type(self).service_class()
        key = f"{srvc_cls.__name__}_{id}"

        object = storage.get(key)
        if not object:
            raise KeyError(f'{srvc_cls.__name__} was not found')
        
        required = srvc_cls.required()

        subset = {
            inputs[key] for key in required and key in inputs.keys()
        }

        object.updated_at = datetime.now()

        # Assigning the values like so ensures we don't skip the
        # validations established in the setter methods
        for key, value in subset.items():
            setattr(object, key, value)

        storage.save()
        return object

    def delete(self, key):
        srvc_cls = type(self).service_class()
        key = f"{srvc_cls.__name__}_{id}"

        object = storage.get(key)
        if not object:
            raise KeyError(f'{srvc_cls.__name__} was not found')
        
        storage.remove(object)
        storage.save()

        return object

    def get(self, id):
        srvc_cls = type(self).service_class()
        key = f"{srvc_cls.__name__}_{id}"
        return storage.get(key)

    def all(self):
        srvc_cls = type(self).service_class()
        return storage.all(srvc_cls.__name__)

    @classmethod
    def service_class(cls):
        return cls.__dict__[f"_{cls.__name__}__service_class"]
