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
IGNORE_DOMAINS = {
    'docs.google.com',
    'jira.2u.com',
    'calendar.google.com',
    'drive.google.com',
    'meet.google.com',
}
