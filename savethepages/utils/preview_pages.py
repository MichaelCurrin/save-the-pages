from lib import connect
from models import Page


connect()
for p in Page.objects():
    print(p)
    print()
