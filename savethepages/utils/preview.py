"""
Preview module.

Show contents of the DB.
"""
import connection
import models


print("Labels")
for l in models.Label.objects:
    print(l)
    print()

print("Pages")
for p in models.Page.objects:
    print(p)
    print()
