#!/bin/bash -e
# Debug assistant.
#
# Start an interactive iPython session with access to the DB models already setup.

source venv/bin/activate
cd savethepages
ipython -i -c 'import connection; import models'
