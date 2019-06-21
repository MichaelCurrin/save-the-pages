"""
Models module.
"""
import datetime

import mongoengine as me


class Label(me.Document):
    """
    Models a label.
    """
    name = me.StringField(max_length=50, unique=True, required=True)


class Page(me.Document):
    """
    Models a webpage and its metadata.

    Given a URL, one can lookup and store HTML content on the collection.
    The other metadata on the object makes it easier to manage than having
    a plain text HTML file on disk.
    """
    title = me.StringField(max_length=200)
    url = me.StringField(max_length=1000)
    content = me.StringField(required=True)
    status_code = me.IntField(max_value=1000)

    label = me.ReferenceField(Label, required=True)

    date_added = me.DateTimeField(default=datetime.datetime.now)
    date_modified = me.DateTimeField(default=datetime.datetime.now)
