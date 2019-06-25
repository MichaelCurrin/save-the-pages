"""
Preview module.

Show contents of the DB.
"""
import connection
import models


print("Labels")
print(models.Label.objects.count())
for l in models.Label.objects[:5]:
    print(l)
    print()

print("Pages")
print(models.Page.objects.count())
for p in models.Page.objects[:5]:
    print(p)
    print()
