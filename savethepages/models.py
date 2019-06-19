import datetime

import mongoengine as me


class Label(me.Document):
    title = me.StringField(max_length=50, unique=True, required=True)


class Page(me.Document):
    title = me.StringField(max_length=200)
    content = me.StringField(required=True)

    label = me.ReferenceField(Label, required=True)

    date_added = me.DateTimeField(default=datetime.datetime.now)
    date_modified = me.DateTimeField(default=datetime.datetime.now)
