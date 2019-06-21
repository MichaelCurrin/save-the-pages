"""
Models module.
"""
import datetime

import mongoengine as me


import lib


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
    url = me.StringField(max_length=1000, required=True)
    content = me.StringField(required=True)
    status_code = me.IntField(max_value=1000)

    label = me.ReferenceField(Label, required=True)

    date_added = me.DateTimeField(default=datetime.datetime.now)
    date_modified = me.DateTimeField(default=datetime.datetime.now)

    def short_url(self):
        return lib.truncate(self.url, width=30)

    def short_content(self, width=80):
        if self.content:
            return lib.truncate(self.content, width)

        return "(not set)"

    def __str__(self):
        """
        Use !r here to return the repr value. For example, string quotes are
        included and newlines are printed as escaped characters.
        """
        return f"<Page: title={self.title!r} status_code={self.status_code!r}"\
               f" url={self.short_url()!r} content={self.short_content(20)!r}>"
