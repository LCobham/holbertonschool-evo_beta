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

    def host_is_valid(self, **inputs):
        from service.user_service import UserService
        host = inputs.get('host')
        usr_srvc = UserService()

        # Use get() method so that no KeyError is raised if user not found
        # and getattr() function just in case that get() returns None 
        if not usr_srvc.get(getattr(host, 'id')):
            raise ValueError('user id not found in storage')

    def city_is_valid(self, **inputs):
        from service.city_service import CityService
        city = inputs.get('city')
        city_srvc = CityService()

        # Use get() method so that no KeyError is raised if user not found
        # and getattr() function just in case that get() returns None 
        if not city_srvc.get(getattr(city, 'id')):
            raise ValueError('city id not found in storage')


    # A bit redundant since City is validated & valid city implies valid country
    def country_is_valid(self, **inputs):
        from service.country_service import CountryService
        country = inputs.get('country')
        country_srvc = CountryService()

        # Use get() method so that no KeyError is raised if user not found
        # and getattr() function just in case that get() returns None 
        if not country_srvc.get(getattr(country, 'id')):
            raise ValueError('country id not found in storage')
        
        # Could also validate that entered country = city.country

    def amenities_are_valid(self, **inputs):
        from service.amenity_service import AmenityService
        amenity_array = inputs.get('amenities')

        if type(amenity_array) is not list or \
            not all(type(amenity) is str for amenity in amenity_array):
            raise TypeError('amenities must be a list of amenity ids')
        
        amenity_srvc = AmenityService()
        all_amenities = amenity_srvc.all()

        for id in amenity_array:
            if f"Amenity_{id}" not in all_amenities.keys():
                raise ValueError('some of the selected amenities were not found')
    
    def reviews_are_valid(self, **inputs):
        from service.review_service import ReviewService
        review_array = inputs.get('reviews')

        if type(review_array) is not list or \
            not all(type(review) is str for review in review_array):
            raise TypeError('reviews must be a list of review ids')
        
        review_srvc = ReviewService()
        all_reviews = review_srvc.all()

        for id in review_array:
            if f"Review_{id}" not in all_reviews.keys():
                raise ValueError('some of the selected reviews were not found')

    def create(self, **inputs):
        self.host_is_valid(**inputs)
        self.country_is_valid(**inputs)
        self.city_is_valid(**inputs)
        self.amenities_are_valid(**inputs)
        self.reviews_are_valid(**inputs)

        return ServiceBase.create(self, **inputs)
    
    def updated(self, id, **inputs):
        input_keys = inputs.keys()

        if 'host' in input_keys:
            self.host_is_valid(**inputs)
        
        if 'country' in input_keys:
            self.country_is_valid(**inputs)
        
        if 'city' in input_keys:
            self.city_is_valid(**inputs)
        
        if 'amenities' in input_keys:
            self.amenities_are_valid(**inputs)
        
        if 'reviews' in input_keys:
            self.reviews_are_valid(**inputs)

        return ServiceBase.update(self, id, **inputs)
