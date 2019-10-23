"""
Test the ability to read a text file and print out the lines.
"""
import lib

path = lib.make_absolute('var/urls.txt')
data = lib.read(path, True)

for x in data:
    print(repr(x))
