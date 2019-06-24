from mongoengine import NotUniqueError

import lib
from models import Page, Label


def main():
    """
    Main command-line function.

    Using a text file, get or fetch a label then create pages, skipping over
    URLs which already exist in the DB, whether from the same or another source.
    """
    import connection

    filename = 'chrome_onetab.txt'
    file_path = f"var/{filename}"

    pages_to_import = lib.handle_onetab_text(file_path)
    label_name = filename
    label = Label.objects(name=label_name).upsert_one(name=label_name)

    for page in pages_to_import:
        url = page['url']
        print(url)

        print(page)
        page_rec = Page(
            title=page['title'],
            url=url,
            label=label,
        )
        try:
            page_rec.save()
        except NotUniqueError:
            print("- exists")
        else:
            print("- added")
        print()


if __name__ == "__main__":
    main()
