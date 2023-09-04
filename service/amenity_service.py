#!/usr/bin/python3
"""
    This module defines the AmenityService class
    with the business logic related to the Amenity
    class
"""

from model.amenity import Amenity
from service.service import ServiceBase


class AmenityService(ServiceBase):
    """
        Amenity Service class for amenity business logic
    """
    __service_class = Amenity

    @classmethod
    def validate_name_is_unique(cls, name):
        all = cls.all().values()

        search_name = list(filter(lambda x: x.name == name, all))
        if search_name:
            raise ValueError('amenity with that name already exists')

    @classmethod
    def create(cls, **inputs):
        if 'name' in inputs.keys():
            cls.validate_name_is_unique(inputs['name'])
        return cls.create_base(**inputs)

    @classmethod
    def update(cls, id, **inputs):
        if 'name' in inputs.keys():
            cls.validate_name_is_unique(inputs['name'])
        return cls.update_base(id, **inputs)
