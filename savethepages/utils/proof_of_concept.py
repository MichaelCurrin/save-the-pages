"""
Proof of concept application file.

Read from a text file, request each URL and store the URL and content in the DB.
"""
import os

import requests

import config
import connection
import lib
from models import Page, Label


def main():
    """
    Main command-line function.
    """
    name = 'Testing'
    label = Label.objects(name=name).upsert_one(name=name)

    lines = lib.read('var/chrome_onetab.txt')
    pages = [dict(zip(('url', 'title'), line.split(' | ', 1))) for line in lines]

    for page in pages[:10]:
        url = page['url']
        print(url)
        resp = requests.get(url)
        print(resp.status_code, resp.reason)
        body = resp.text
        print(len(body))

        page_rec = Page(
            title=page['title'],
            url=url,
            content=body,
            status_code=resp.status_code,
            label=label,
        )
        page_rec.save()
        print()


if __name__ == '__main__':
    main()
