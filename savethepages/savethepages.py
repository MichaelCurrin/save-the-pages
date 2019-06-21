"""
Main application file.
"""
import os

import requests

import config
import lib
from models import Page, Label


def main():
    name = 'Chrome work testing'
    label = Label.objects(name=name).first()
    label = Label.objects(name=name).upsert_one(name=name)

    with open(os.path.join(config.APP_DIR, 'var/urls.txt')) as f_in:
        pages = [dict(zip(('url', 'title'), line.split(' | ', 1)))
                 for line in f_in]

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
    lib.connect()
    main()
