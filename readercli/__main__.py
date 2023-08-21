"""Provides code to interact with the Reader API in the command-line"""
import argparse

from rich import print

from .api import fetch_documents, add_document
from .reading_list import load_reading_list
from .constants import VALID_LOCATION_OPTIONS
from .utils import count_category_values

# Use a dictionary for location options and descriptions
LOCATION_DESCRIPTIONS = {
    "new": "New Documents",
    "later": "Later Documents",
    "archive": "Archived Documents",
    "feed": "Feed Documents",
}


def main():
    parser = argparse.ArgumentParser(
        description="Save or List Documents from Readwise Reader",
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    list_parser = subparsers.add_parser("list", help="List Documents")
    list_parser.add_argument("-d", "--days", help="Updated after in days.")
    list_parser.add_argument(
        "-l",
        "--location",
        choices=VALID_LOCATION_OPTIONS,
        help="Document location: `new`, `later`, `archive`, `feed`",
    )

    import_parser = subparsers.add_parser("import", help="Import Chrome Reading List")
    import_parser.add_argument("-f", "--file", help="File path or name for HTML file")

    add_parser = subparsers.add_parser("add", help="Add Document(s)")
    add_parser.add_argument("-f", "--file", help="File path or name for HTML file")
    add_parser.add_argument("-u", "--url", help="URL string for the document")

    args = parser.parse_args()

    if args.command == "list":
        try:
            if args.location or args.days:
                if args.days:
                    try:
                        days = int(args.days)
                    except ValueError as e:
                        print("Error: ", e)
                        days = None  # switch to None if user inputs a incorrect value that's not an int
                else:
                    days = args.days
                full_data = fetch_documents(location=args.location, updated_after=days)
            else:
                full_data = fetch_documents()
            print(full_data)
            print("Number of documents:", len(full_data))
            print("Category breakdown:", count_category_values(full_data))
        except ValueError as e:
            print("Error:", e)
            if args.location not in VALID_LOCATION_OPTIONS:
                print(f"'{args.location}' is not a valid location for Documents.")
                print("Try:", ", ".join(LOCATION_DESCRIPTIONS.keys()))

    elif args.command == "import":
        print("Importing Reading List...")
        reading_list = load_reading_list(args.file)
        print(reading_list)

    elif args.command == "add":
        if args.file:
            print(f"Adding Document(s) from file: {args.file}")
            reading_list = load_reading_list(args.file)
            documents_to_add = [{"url": document.url} for document in reading_list]
            add_document_batch(documents_to_add)
        elif args.url:
            print(f"Adding Document from URL: {args.url}")
            add_document(data={"url": args.url})
        else:
            print("No file or URL specified.")

    else:
        parser.print_help()


def add_document_batch(documents: list[dict]) -> None:
    for document in documents:
        add_document(data={"url": document.url})


if __name__ == "__main__":
    main()
