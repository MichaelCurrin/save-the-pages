from lib import connect
import models


connect()

print("Labels")
for l in models.Label.objects():
    print(l)
    print()

print("Pages")
for p in models.Page.objects():
    print(p)
    print()
