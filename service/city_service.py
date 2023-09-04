#!/usr/bin/python3
"""
    This module defines the CityService class
    with the business logic related to the City
    class
"""

from model.city import City
from service.service import ServiceBase


class CityService(ServiceBase):
    """
        City service class for City business logic
    """
    __service_class = City

    @staticmethod
    def country_is_valid(country_id):
        from service.country_service import CountryService

        if not CountryService.get(country_id):
            raise ValueError('country id not found in storage')

    @classmethod
    def create(cls, **inputs):
        from service.country_service import CountryService

        if 'country' in inputs.keys():
            CityService.country_is_valid(inputs['country'])

        # Create new city
        new_city = CityService.create_base(**inputs)

        # Add city to the list of cities of the country
        country = CountryService.get(inputs.get('country'))

        # Sanity check. But this is checked in create_base
        if not country:
            raise AttributeError('country not found')

        updated_cities = country.cities
        updated_cities.append(new_city.id)

        CountryService.update(country.id, **{'cities': updated_cities})

        return new_city

    @classmethod
    def update(cls, id, **inputs):
        if 'country' in inputs.keys():
            cls.country_is_valid(inputs['country'])

        return cls.update_base(id, **inputs)
