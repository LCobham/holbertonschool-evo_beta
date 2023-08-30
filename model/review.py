#!/usr/bin/python3
"""
    This module defines the Review class for
    the AitBnB project
"""

from model.base import BaseModel
from datetime import datetime


class Review(BaseModel):
    """
        Review class for AirBnB
        Attrs:
            - id (string): UUID4 
            - created_at (datetime): datetime of creation
            - updated_at (datetime): datetime of last update
            - user (string): user ID of who's leaving the review
            - place (string): place (ID) that's being reviewed
            - rating (int): rating of the review
            - comment (string): comment associated to the review
    """
    def __init__(self, user, place, rating, comment):
        BaseModel.__init__(self)
        self.user = user
        self.place = place
        self.rating = rating
        self.comment = comment

    @classmethod
    def constructor(cls, dictionary):
        required = {
            'user': dictionary.get('user'),
            'place': dictionary.get('place'),
            'rating': dictionary.get('rating'),
            'comment': dictionary.get('comment')
            }

        new_review = cls(**required)
        keys = dictionary.keys()

        if '__class__' in keys:
            del dictionary['__class__']

        if 'created_at' in keys and type(dictionary['created_at']) is datetime:
            dictionary['created_at'] = \
                datetime.fromisoformat(dictionary['created_at'])

        if 'updated_at' in keys and type(dictionary['updated_at']) is datetime:
            dictionary['updated_at'] = \
                datetime.fromisoformat(dictionary['updated_at'])

        new_review.__dict__.update(dictionary)
        return new_review
