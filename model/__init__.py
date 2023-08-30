#!/usr/bin/python3
"""
    This module makes the files inside this directory behave as a package
    and it also defines key variables for the rest of the program.
"""
from model.user import User
from model.amenity import Amenity
from model.place import Place
from model.country import Country
from model.city import City
from model.review import Review

classes = {
    'User': User,
    'Amenity': Amenity,
    'Place': Place,
    'Country': Country,
    'City': City,
    'Review': Review
}
