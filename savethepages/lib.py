"""
Library module.
"""
from mongoengine import connect as mongo_connect

import config


def connect():
    """
    Connect to a MongoDB with configured credentials.

    :return: DB connection object of type <class 'pymongo.mongo_client.MongoClient'>.
    """
    return mongo_connect(**config.CONNECTION)


def connect_and_drop():
    """
    Drop the configured database name and return a connection to it.

    :return: DB connection object of type <class 'pymongo.mongo_client.MongoClient'>.
    """
    print("Connecting to DB")
    db = connect()

    print("Dropping DB")
    db.drop_database(config.CONNECTION['db'])

    return db


def truncate(text, width=80):
    """
    Return text truncate to given width with ellipsis if other length.

    The builting textwrap.shortern does not work here if the value is a single
    long word (e.g. a URL) as the entire URL is replaced with '[...]'.

    https://stackoverflow.com/questions/2872512/python-truncate-a-long-string/34993870

    Handles ed
    """
    placeholder = "[...]"
    if width < len(placeholder):
        raise ValueError(f"width must at least be as long as the placeholder length: {len(placeholder)}")

    if len(text) > width:
        return f"{text[:width - len(placeholder)]}{placeholder}"

    return text
