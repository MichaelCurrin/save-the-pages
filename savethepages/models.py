"""
Models module.
"""
import datetime

import mongoengine as me


class Label(me.Document):
    name = me.StringField(max_length=50, unique=True, required=True)


class Page(me.Document):
    title = me.StringField(max_length=200)
    url = me.StringField(max_length=1000)
    content = me.StringField(required=True)
    status_code = me.IntField(max_value=1000)

    label = me.ReferenceField(Label, required=True)

    date_added = me.DateTimeField(default=datetime.datetime.now)
    date_modified = me.DateTimeField(default=datetime.datetime.now)
