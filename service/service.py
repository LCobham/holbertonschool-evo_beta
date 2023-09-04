#!/usr/bin/python3
"""
    This module creates an interface for the
    Services Classes in the AirBnB project
"""

from abc import ABC, abstractclassmethod
from model import storage
from datetime import datetime


class ServiceBase(ABC):
    """
        Interface for the Services Classes
        Class Attrs:
            - __service_class: class to which the service is provided
            (ex: UserService -> __service_class = User)
        Methods:
            - create_base: Basic "create" functionality. Made so that
            create method can be extended by performing some class-specific
            validations before calling cls.create_base().
            - update_base: Base for update functionality. Updates the fields
            of an object in storage. Made so that update mathod extends this
            core functionality.
            - get: Gets an item from the storage with a given key
            - delete: Deletes an item from the storage
    """
    __service_class = None

    @abstractclassmethod
    def create(cls, **inputs):
        pass

    @abstractclassmethod
    def update(cls, **inputs):
        pass

    @classmethod
    def create_base(cls, **inputs):
        service_cls = cls.service_class()
        required_inputs = service_cls.required()

        # Get only relevant information
        subset = {key: inputs[key] for key in required_inputs}

        new_instance = service_cls(**subset)
        storage.add(new_instance)
        storage.save()

        return new_instance

    @classmethod
    def update_base(cls, id, **inputs):
        srvc_cls = cls.service_class()

        key = f"{srvc_cls.__name__}_{id}"

        object = storage.get(key)
        if not object:
            raise KeyError(f'{srvc_cls.__name__} was not found')
        
        required = srvc_cls.required()

        intersection = list(set(required).intersection(inputs.keys()))

        subset = { key: inputs[key] for key in intersection }

        object.updated_at = datetime.now()

        # Assigning the values like so ensures we don't skip the
        # validations established in the setter methods
        for key, value in subset.items():
            setattr(object, key, value)

        storage.save()
        return object

    @classmethod
    def delete(cls, id):
        srvc_cls = cls.service_class()
        key = f"{srvc_cls.__name__}_{id}"

        object = storage.get(key)
        if not object:
            raise KeyError(f'{srvc_cls.__name__} was not found')
        
        storage.remove(object)
        storage.save()

        return object

    @classmethod
    def get(cls, id):
        srvc_cls = cls.service_class()
        key = f"{srvc_cls.__name__}_{id}"
        return storage.get(key)

    @classmethod
    def all(cls):
        srvc_cls = cls.service_class()
        return storage.all(srvc_cls.__name__)

    @classmethod
    def service_class(cls):
        return cls.__dict__[f"_{cls.__name__}__service_class"]
