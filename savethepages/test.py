
import lib
from models import Page, Label

lib.connect()


def test():
    label = Label.objects(title='_testing').modify(title='_testing')
    post = Page(
        title="TWO",
        content="<div>",
        label=label
    )
    post.save()
    print(post)


if __name__ == "__main__":
    test()
