#!/usr/bin/python3
"""
    This module defines the PlaceService class
    with the business logic related to the Place
    class
"""

from model.place import Place
from service.service import ServiceBase


class PlaceService(ServiceBase):
    """
        Place service class for Place business logic
    """
    __service_class = Place

    @staticmethod
    def host_is_valid(host_id):
        from service.user_service import UserService

        if not UserService.get(host_id):
            raise ValueError('user id not found in storage')

    @staticmethod
    def city_is_valid(city_id):
        from service.city_service import CityService

        if not CityService.get(city_id):
            raise ValueError('city id not found in storage')

    # A bit redundant since City is validated & valid city
    # implies valid country
    @staticmethod
    def country_is_valid(country_id):
        from service.country_service import CountryService

        if not CountryService.get(country_id):
            raise ValueError('country id not found in storage')

        # Could also validate that entered country = city.country

    @staticmethod
    def amenities_are_valid(amenity_array):
        from service.amenity_service import AmenityService

        if type(amenity_array) is not list or \
                not all(type(amenity) is str for amenity in amenity_array):
            raise TypeError('amenities must be a list of amenity ids')

        all_amenities = AmenityService.all()

        for id in amenity_array:
            if f"Amenity_{id}" not in all_amenities.keys():
                raise ValueError(
                    'some of the selected amenities were not found'
                    )

    @staticmethod
    def reviews_are_valid(review_array):
        from service.review_service import ReviewService

        if type(review_array) is not list or \
                not all(type(review) is str for review in review_array):
            raise TypeError('reviews must be a list of review ids')

        review_srvc = ReviewService()
        all_reviews = review_srvc.all()

        for id in review_array:
            if f"Review_{id}" not in all_reviews.keys():
                raise ValueError('some of the selected reviews were not found')

    @classmethod
    def create(cls, **inputs):
        input_keys = inputs.keys()

        if 'host' in input_keys:
            cls.host_is_valid(inputs['host'])

        if 'country' in input_keys:
            cls.country_is_valid(inputs['country'])

        if 'city' in input_keys:
            cls.city_is_valid(inputs['city'])

        if 'amenity' in input_keys:
            cls.amenities_are_valid(inputs['amenities'])

        # When a place is created, it has no reviews
        inputs['reviews'] = []

        return cls.create_base(**inputs)

    @classmethod
    def update(cls, id, **inputs):
        input_keys = inputs.keys()

        if 'host' in input_keys:
            cls.host_is_valid(inputs['host'])

        if 'country' in input_keys:
            cls.country_is_valid(inputs['country'])

        if 'city' in input_keys:
            cls.city_is_valid(inputs['city'])

        if 'amenity' in input_keys:
            cls.amenities_are_valid(inputs['amenities'])

        if 'reviews' in input_keys:
            cls.reviews_are_valid(inputs['reviews'])

        return cls.update_base(id, **inputs)
