"""
Fetch application file.

Request URLs in the DB and store the response data.
"""
import requests

import connection
from models import Page


def request_page(url):
    """
    Attempt to request a given URL and return response data on any result.
    """
    content = None
    status_code = None
    error_message = None

    try:
        resp = requests.get(url, timeout=10)
    except requests.Timeout as e:
        error_message = 'timeout'
    except requests.URLRequired:
        error_message = 'URL required'
    except requests.TooManyRedirects:
        error_message = 'Too many redirects'
    except requests.RequestException as r:
        error_message = f"Other request error - {r}"
    else:
        content = resp.text
        status_code = resp.status_code

    return content, status_code, error_message


requested = 0
skipped = 0
for page in Page.objects:
    if page.attempted:
        skipped += 1
    else:
        requested += 1
        print(f"Fetch: {page.short_url()}")
        content, status_code, error_message = request_page(page.url)

        page.content = content
        page.status_code = status_code
        page.error_message = error_message
        page.save()
        succeeded, message = page.outcome()
        if not succeeded:
            print(message)

print(f"\nRequested: {requested:,d}")
print(f"Skipped: {skipped:,d}")
