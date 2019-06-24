"""
Tutorial application.

Standalone script to show how to connect to MongoDB, define a model and
do a valid and invalid operation on it.

Code used from an introductory tutorial on Python and Mongo:
    https://realpython.com/introduction-to-mongodb-and-python/
"""
import datetime

from mongoengine import *
connect('mongoengine_test', host='localhost', port=27017)


class Post(Document):
    title = StringField(required=True, max_length=200)
    content = StringField(required=True)
    author = StringField(required=True, max_length=50)
    published = DateTimeField(default=datetime.datetime.now)

    @queryset_manager
    def live_posts(self, queryset):
        return queryset.filter(published=True)


def main():
    post_1 = Post(
        title='Sample Post',
        content='Some engaging content',
        author='Scott'
    )
    post_1.save()       # This will perform an insert
    print(post_1.title)
    post_1.title = 'A Better Post Title'
    post_1.save()       # This will perform an atomic edit on "title"
    print(post_1.title)

    post_2 = Post(content='Content goes here', author='Michael')
    try:
        post_2.save()
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
