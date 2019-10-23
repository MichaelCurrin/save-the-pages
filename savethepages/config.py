"""
Config module.
"""
import os


CONNECTION = dict(
    db='savethepages',
    host='localhost',
    port=27017,
)

APP_DIR = os.path.dirname(__file__)

# Ignore chrome, ftp and others.
USE_PROTOCOLS = {
    'https',
    'http'
}
# How to make sure ignores are marked as ignore status? Or not? no flag so they always skipped until the rule changes
# but you want to know it was considered else won't no easily. or should be marked as delete?
# I also want to manually delete these after import?
IGNORE_DOMAINS = {
    'docs.google.com',
    'jira.2u.com',
    'calendar.google.com',
    'drive.google.com',
    'meet.google.com',
    'rpm.newrelic.com',
    'www.youtube.com/',
}
