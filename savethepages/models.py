"""
Models module.
"""
import datetime
from urllib import parse

import mongoengine as me

import config
import lib


URL_MAX = 1000

class Label(me.Document):
    """
    Models a webpage label.

    Describe the source of a URL. The name should contain something
    useful like the browser, whether it is history/bookmarks/OneTab export,
    the date, whether it is personal/work device or if it was a manual entry.
    """
    name = me.StringField(max_length=50, unique=True, required=True)

    def __str__(self):
        return f"name={self.name!r}"


class Page(me.Document):
    """
    Models a webpage which has content and metadata.

    Given a URL, one can lookup and store HTML content on the collection.
    The other metadata on the object makes it easier to manage than having
    a plain text HTML file on disk.

    If a site cannot be reached, we expect error message to be filled
    and content and status code to be None still.
    If site can be reached, we expect content to be filled and statuse code
    to be a 2XX for success, 3XX for moved or 4XX-5XX for errors.
    """
    title = me.StringField(max_length=1000)
    url = me.StringField(max_length=URL_MAX, unique=True, required=True)

    content = me.StringField()
    status_code = me.IntField(max_value=1000)
    # For sites that cannot be reached to give a status code.
    error_message = me.StringField(max_length=1000)

    # Create a link to a single Label and delete pages after the label is
    # deleted, but at the DB level do not nest/embed in the pages in the label.
    label = me.ReferenceField(Label, reverse_delete_rule=me.CASCADE,
                              required=True)

    created_at = me.DateTimeField(default=datetime.datetime.now)
    modified_at = me.DateTimeField(default=datetime.datetime.now)

    def unpack_url(self):
        """
        Return tuple of protocol and domain.
        """
        u = parse.urlsplit(self.url)

        return u.scheme, u.netloc

    def is_useful(self):
        """
        Determine whether a URL is worth fetching.
        """
        protocol, domain = self.unpack_url()
        if protocol not in config.USE_PROTOCOLS:
            return False
        # Ignore anything with a port as it is probably something like
        # localhost or something requiring authorization.
        if domain in config.IGNORE_DOMAINS or ":" in domain:
            return False

        return True


    @property
    def attempted(self):
        """
        Signal whether an attempt has been made to store a response for the URL.
        """
        if self.error_message or self.status_code:
            return True

        return False

    def outcome(self):
        if self.error_message:
            return False, self.error_message
        if self.status_code >= 300:
            return False, self.status_code

        return True, self.status_code

    def clean(self):
        """
        Execute on updating objects.
        """
        self.modified_at = datetime.datetime.now()

    def short_title(self, width=70):
        return lib.truncate(self.title, width)

    def short_url(self, width=70):
        return lib.truncate(self.url, width)

    def short_content(self, width=70):
        return lib.truncate(self.content, width)

    def __str__(self):
        """
        Use !r here to return the repr value. For example, string quotes are
        included and newlines are printed as escaped characters.
        """
        return (
            f"title={self.short_title()!r} "
            f"\nurl={self.short_url()!r}"
            f"\ncontent={self.short_content()!r}"
            f"\nstatus_code={self.status_code!r}"
            f"\nerror_message={self.error_message!r}"
        )
