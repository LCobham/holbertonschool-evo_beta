#!/usr/bin/python3
"""
    This module defines the CityService class
    with the business logic related to the City
    class
"""

from model.city import City
from service.country_service import CountryService
from service.service import ServiceBase


class CityService(ServiceBase):
    """
        City service class for City business logic
    """
    __service_class = City

    def country_is_valid(self, **inputs):
        country = inputs.get('country')
        country_svc = CountryService()

        # Use get() method so that no KeyError is raised if user not found
        # and getattr() function just in case that get() returns None 
        if not country_svc.get(getattr(country, 'id')):
            raise ValueError('country id not found in storage')

    def create(self, **inputs):
        self.country_is_valid(**inputs)
        return ServiceBase.create(self, **inputs)
            

    def update(self, id, **inputs):
        if 'country' in inputs.keys():
            self.country_is_valid(**inputs)

        return ServiceBase.update(id, **inputs)
