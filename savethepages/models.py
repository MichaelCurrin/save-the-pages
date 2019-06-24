"""
Models module.
"""
import datetime

import mongoengine as me

import lib


class Label(me.Document):
    """
    Models a webpage label.

    Describe the source of a URL. The name should contain something
    useful like the browser, whether it is history/bookmarks/OneTab export,
    the date, whether it is personal/work device or if it was a manual entry.
    """
    name = me.StringField(max_length=50, unique=True, required=True)

    def __str__(self):
        return f"<Label: name={self.name!r} >"


class Page(me.Document):
    """
    Models a webpage which has content and metadata.

    Given a URL, one can lookup and store HTML content on the collection.
    The other metadata on the object makes it easier to manage than having
    a plain text HTML file on disk.
    """
    title = me.StringField(max_length=300)
    url = me.StringField(max_length=1000, unique=True, required=True)

    content = me.StringField()
    status_code = me.IntField(max_value=1000)

    label = me.ReferenceField(Label, required=True)

    created_at = me.DateTimeField(default=datetime.datetime.now)
    modified_at = me.DateTimeField(default=datetime.datetime.now)

    def clean(self):
        self.modified_at = datetime.datetime.now()

    def short_url(self, width=70):
        return lib.truncate(self.url, width)

    def short_content(self, width=70):
        if self.content:
            return lib.truncate(self.content, width)

        return "(not set)"

    def __str__(self):
        """
        Use !r here to return the repr value. For example, string quotes are
        included and newlines are printed as escaped characters.
        """
        return (
            f"<Page:"
            f"\n title={self.title!r} \n status_code={self.status_code!r}"
            f"\n url={self.short_url()!r} \n content={self.short_content()!r}"
            f"\n >"
        )
