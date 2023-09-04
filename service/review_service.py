#!/usr/bin/python3
"""
    This module defines the ReviewService class
    with the business logic related to the Review
    class
"""

from model.review import Review
from service.service import ServiceBase
from model import storage
from datetime import datetime


class ReviewService(ServiceBase):
    """
        Review service class for Review business logic
    """
    __service_class = Review

    @staticmethod
    def user_is_valid(**inputs):
        from service.user_service import UserService
        usr = inputs.get('user')
        usr_srvc = UserService()

        # Use get() method so that no KeyError is raised if user not found
        # and getattr() function just in case that get() returns None 
        if not usr_srvc.get(getattr(usr, 'id')):
            raise ValueError('user id not found in storage')

    @staticmethod
    def place_is_valid(**inputs):
        from service.place_service import PlaceService
        place = inputs.get('place')
        place_srvc = PlaceService()

        # Use get() method so that no KeyError is raised if user not found
        # and getattr() function just in case that get() returns None 
        if not place_srvc.get(getattr(place, 'id')):
            raise ValueError('user id not found in storage')        

    @classmethod
    def create(cls, **inputs):
        from service.place_service import PlaceService

        cls.user_is_valid(**inputs)
        cls.place_is_valid(**inputs)

        new_review = cls.create_base(cls, **inputs)

        # When a review is created, add to the list of reviews of that place
        place = PlaceService.get(inputs.get('place'))

        updated_reviews = place.reviews.update({new_review.key: new_review})

        PlaceService.update(place.id,**{'reviews': updated_reviews})

        return new_review

    @classmethod
    def updated(self, id, **inputs):
        # Modified this method so that only comment and rating can be updated
        # but not the place id not the user id

        srvc_cls = type(self).service_class()
        key = f"{srvc_cls.__name__}_{id}"

        object = storage.get(key)
        if not object:
            raise KeyError(f'{srvc_cls.__name__} was not found')
        
        required = ('comment', 'rating')
        intersection = list(set(required).intersection(inputs.keys()))

        subset = { key: inputs[key] for key in intersection }

        object.updated_at = datetime.now()

        # Assigning the values like so ensures we don't skip the
        # validations established in the setter methods
        for key, value in subset.items():
            setattr(object, key, value)

        storage.save()
        return object
