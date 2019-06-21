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
