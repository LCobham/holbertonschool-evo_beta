#!/usr/bin/python3
"""
    This module defines the AmenityService class
    with the business logic related to the Amenity
    class
"""

from model.amenity import Amenity
from service.service import ServiceBase


class AmenityService(ServiceBase):
    """
        Amenity Service class for amenity business logic
    """
    __service_class = Amenity
