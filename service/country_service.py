#!/usr/bin/python3
"""
    This module defines the CountryService class
    with the business logic related to the Country
    class
"""

from model.country import Country
from service.service import ServiceBase


class CountryService(ServiceBase):
    """
        Country service class for Country business logic
    """
    __service_class = Country

    @classmethod
    def create(cls, **inputs):
        # Ensure countries have 0 cities at creation
        inputs['cities'] = []
        return cls.create_base(**inputs)
    
    @classmethod
    def update(cls, id, **inputs):
        return cls.update_base(id, **inputs)
