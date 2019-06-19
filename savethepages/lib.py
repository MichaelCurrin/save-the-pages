from mongoengine import connect as mongo_connect

import config


def connect():
    mongo_connect(**config.CONNECTION)
