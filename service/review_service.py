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

    def user_is_valid(self, **inputs):
        from service.user_service import UserService
        usr = inputs.get('user')
        usr_srvc = UserService()

        # Use get() method so that no KeyError is raised if user not found
        # and getattr() function just in case that get() returns None 
        if not usr_srvc.get(getattr(usr, 'id')):
            raise ValueError('user id not found in storage')

    def place_is_valid(self, **inputs):
        from service.place_service import PlaceService
        place = inputs.get('place')
        place_srvc = PlaceService()

        # Use get() method so that no KeyError is raised if user not found
        # and getattr() function just in case that get() returns None 
        if not place_srvc.get(getattr(place, 'id')):
            raise ValueError('user id not found in storage')        

    def create(self, **inputs):
        from service.place_service import PlaceService

        self.user_is_valid(**inputs)
        self.place_is_valid(**inputs)

        new_review = ServiceBase.create(self, **inputs)

        # When a review is created, add to the list of reviews of that place
        place_srvc = PlaceService()
        place = place_srvc.get(inputs.get('place'))

        updated_reviews = place.reviews.update({new_review.key: new_review})

        place_srvc.update(place.id,**{'reviews': updated_reviews})

        return new_review

    def updated(self, id, **inputs):
        # Modified this method so that only comment and rating can be updated
        # but not the place id not the user id

        srvc_cls = type(self).service_class()
        key = f"{srvc_cls.__name__}_{id}"

        object = storage.get(key)
        if not object:
            raise KeyError(f'{srvc_cls.__name__} was not found')
        
        required = ('comment', 'rating')

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
