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
    __required = ('user', 'place', 'rating', 'comment')

    def __init__(self, user, place, rating, comment):
        BaseModel.__init__(self)
        self.__user = user
        self.__place = place
        self.__rating = rating
        self.__comment = comment

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        if type(user) is not str:
            raise TypeError('user must be a (string) user ID')
        self.__user = user

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, place):
        if type(place) is not str:
            raise TypeError('place must be a (string) place ID')
        self.__place = place

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, rating):
        if type(rating) is not int or \
                rating < 0 or rating > 10:
            raise TypeError('rating must be an int between 0 and 10')
        self.__rating = rating

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, comment):
        if type(comment) is not str:
            raise TypeError('comment must be a string')
        self.__comment = comment
