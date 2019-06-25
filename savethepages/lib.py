"""
Library module.
"""
import os

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
    """
    if not text:
        return None

    placeholder = "[...]"
    if width < len(placeholder):
        raise ValueError("width must at least be as long as the placeholder"
                         f" length: {len(placeholder)}")

    if len(text) > width:
        return f"{text[:width - len(placeholder)]}{placeholder}"

    return text


def make_absolute(path):
    """
    Make a path to a path relative to the app directory absolute.
    """
    return os.path.join(config.APP_DIR, path)


def read(file_path, app_relative=True, exclude_empty_lines=True):
    """
    Return contents of a text file.

    Read a text file and return as list of strings, excluding trailing
    newline characters.

    Note that in order to use the splitlines method on a single string from
    the input, the entire file will be read into memory at once.

    :param app_relative: If True, the file_path argument is expected to be relative
        to the project's app directory and should be converted to an absolute
        path. If False, then the path is already a full path.
    :param exclude_empty_lines: If True, filter out lines which are empty.

    :return lines: list of str objects.
    """
    if app_relative:
        file_path = make_absolute(file_path)

    with open(file_path) as f_in:
        text = f_in.read()

    lines = text.splitlines(keepends=False)

    if exclude_empty_lines:
        lines = [l for l in lines if l]

    return lines


def handle_onetab_text(file_path):
    """
    Extract URL data from a text export created from the OneTab extension.
    """
    lines = read(file_path)

    # Zip longest
    return [dict(zip(('url', 'title'), line.split(' | ', 1))) for line in lines]
