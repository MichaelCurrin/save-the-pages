"""
Import URLs application file.
"""
from urllib import parse

from mongoengine import NotUniqueError

import lib
from models import URL_MAX, Label, Page


def upsert_label(name):
    labels = Label.objects(name=name)
    if labels.count():
        return labels.first()

    return labels.upsert_one(name=name)


def insert_page(page_data, label):
    """
    Insert a page record into the DB with given data and label object.

    :return: None
    """
    url = page_data['url']
    # Do this here as adding a look is more involved and on save or validate
    # might not be the right place.
    if len(url) > URL_MAX:
        url_data = parse.urlsplit(url)
        url_data = url_data._replace(path='', query='')
        url = parse.urlunsplit(url_data)

    page = Page(
        title=page_data.get('title'),
        url=url,
        label=label,
    )
    try:
        page.save()
    except NotUniqueError:
        print("exists")
    else:
        print("added")


def load(label_name, pages_to_import):
    """
    Bulk load pages into the DB with a given label.

    Note that the bulk insert operation will not work in mongoengine.
    """
    label = upsert_label(label_name)
    print(repr(label))

    i = -1
    for i, page_data in enumerate(pages_to_import):
        print(i+1)
        try:
            insert_page(page_data, label)
        except Exception:
            print(page_data)
            raise


def main():
    """
    Main command-line function.

    Using a text file, get or fetch a label then create pages, skipping over
    URLs which already exist in the DB, whether from the same or another source.
    """
    import connection

    filename = 'chrome_onetab.txt'
    file_path = f"var/{filename}"

    pages_to_import = lib.handle_onetab_text(file_path)
    load(filename, pages_to_import)


if __name__ == "__main__":
    main()
