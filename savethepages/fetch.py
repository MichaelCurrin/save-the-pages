"""
Fetch application file.

Request URLs in the DB and store the response data.
"""
import requests

import connection
from models import Page


TIMEOUT = 10


def request_page(url):
    """
    Attempt to request a given URL and return response data on any result.
    """
    content = None
    status_code = None
    error_message = None

    try:
        resp = requests.get(url, timeout=TIMEOUT)
    except requests.Timeout:
        error_message = 'timeout'
    except requests.URLRequired:
        error_message = 'URL required'
    except requests.TooManyRedirects:
        error_message = 'Too many redirects'
    except requests.RequestException as e:
        error_message = f"Other request error - {str(e)}"
    else:
        content = resp.text
        status_code = resp.status_code

    return content, status_code, error_message


passed = 0
failed = 0
not_useful = 0
previously_attempted = 0

try:
    for page in Page.objects:
        if not page.is_useful():
            not_useful += 1
        elif page.attempted:
            previously_attempted += 1
        else:
            print(f"Fetch: {page.short_url()}")

            content, status_code, error_message = request_page(page.url)

            page.content = content
            page.status_code = status_code
            page.error_message = error_message
            page.save()

            succeeded, message = page.outcome()

            if succeeded:
                passed += 1
            else:
                failed += 1
                print(message)
finally:
    print("RESULTS")
    print(f"Passed              : {passed:4,d}")
    print(f"Failed              : {failed:4,d}")
    print(f"Not useful          : {not_useful:4,d}")
    print(f"Previously attempted: {previously_attempted:4,d}")
