"""
Test application.

Test the basic upsert logic and the model.
"""
import lib
from models import Page, Label

lib.connect()


def main():
    label = Label.objects(name='_testing').upsert_one(name='_testing')
    post = Page(
        title="TWO",
        content="<div>",
        label=label
    )
    post.save()
    print(post)


if __name__ == "__main__":
    main()
