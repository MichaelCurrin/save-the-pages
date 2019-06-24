"""
Test application.

Test the basic upsert logic and the model.
"""
import lib
from models import Page, Label


def main():
    import connection

    label = Label.objects(name='_testing').upsert_one(name='_testing')

    post1 = Page(
        title="Foo",
        content="<div>Foo bar</div>",
        url='https://foo.bar.com',
        label=label
    )
    print(repr(post1))
    post1.save()
    print()

    post2 = Page(
        title="Bar",
        content="<div>Fizz</div>",
        url='https://fub.buzz.com',
        label=label
    )
    print(repr(post2))
    post2.save()
    print()

    posts = Page.objects(label=label)
    print(posts.count())
    print(posts)
    print()

    print("Deleting")
    post1.delete()
    post2.delete()


if __name__ == "__main__":
    main()
