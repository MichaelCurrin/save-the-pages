"""
Library module.
"""
from mongoengine import connect as mongo_connect

import config


def connect():
    """
    Connect to a MongoDB with configured credentials.

    :return: None
    """
    mongo_connect(**config.CONNECTION)
