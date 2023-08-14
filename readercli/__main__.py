"""Provides code to interact with the Reader API in the command-line"""
import argparse

from readercli.api import fetch_reader_document_list_api, add_document
from readercli.reading_list import load_reading_list
from readercli.constants import VALID_LOCATION_OPTIONS


def main():
    parser = argparse.ArgumentParser(
        description="Save or List Documents from Readwise Reader",
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    list_parser = subparsers.add_parser("list", help="List Documents")
    list_parser.add_argument(
        "-l", "--location", help="Document location: `new`, `later`, `archive`, `feed`"
    )
    import_parser = subparsers.add_parser("import", help="Import Chrome Reading List")
    import_parser.add_argument("-f", "--file", help="File path or name for HTML file")

    add_parser = subparsers.add_parser("add", help="Add Document(s)")
    add_parser.add_argument("-f", "--file", help="File path or name for HTML file")
    add_parser.add_argument("-u", "--url", help="URL string for the document")

    args = parser.parse_args()

    if args.command == "list":
        if args.location in VALID_LOCATION_OPTIONS:
            print(f"Fetching Document list from: {args.location}")
            full_data = fetch_reader_document_list_api(location=args.location)
            print(full_data)
        else:
            print(f"`{args.location}` is not a valid location for Documents.")
            print("Try: `new`, `later`, `archive`, `feed`")

    elif args.command == "import":
        print("Importing Reading List...")
        reading_list = load_reading_list(args.file)
        print(reading_list)
    elif args.command == "add":
        if args.file:
            print(f"Adding Document(s) from file: {args.file}")
            reading_list = load_reading_list(args.file)
            for document in reading_list:
                add_document(data={"url": document.url})
        elif args.url:
            print(f"Adding Document from URL: {args.url}")
            add_document(data={"url": args.url})
        else:
            print("No file or URL specified.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
