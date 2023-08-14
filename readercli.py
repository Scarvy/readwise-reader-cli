"""Provides code to interact with the Reader API in the command-line"""
import argparse

from api import fetch_reader_document_list_api, add_document
from reading_list import load_reading_list
from constants import VALID_LOCATION_OPTIONS

parser = argparse.ArgumentParser(
    description="Save or List Documents from Readwise Reader",
)
subparsers = parser.add_subparsers(dest="command", required=True)

list_parser = subparsers.add_parser("list", help="List Document(s)s")
list_parser.add_argument(
    "-l", "--location", help="Document location: `new`, `later`, `archive`, `feed`"
)
import_parser = subparsers.add_parser("import", help="Import Chrome Reading List")

add_parser = subparsers.add_parser("add", help="Add Document(s)")
add_parser.add_argument("-f", "--file", help="File path or name for HTML file")
add_parser.add_argument("-u", "--url", help="URL string for the document")

args = parser.parse_args()

if args.command == "list":
    if args.location in VALID_LOCATION_OPTIONS:
        print(f"Fetching Document list from: {args.location}")
        # full_data = fetch_reader_document_list_api(location=args.location)

elif args.command == "import":
    print("Importing Reading List...")
    # load_reading_list()
elif args.command == "add":
    if args.file:
        # add_document(file_path=args.file)
        print(f"Adding Document(s) from file: {args.file}")
    elif args.url:
        # add_document(url=args.url)
        print(f"Adding Document(s) from URL: {args.url}")
    else:
        print("No file or URL specified.")
else:
    parser.print_help()
