import argparse

# from api import fetch_reader_document_list_api, add_document

parser = argparse.ArgumentParser(
    description="Save or List Documents from Readwise Reader",
)
subparsers = parser.add_subparsers(dest="command", required=True)

list_parser = subparsers.add_parser("list", help="List Document(s)s")

add_parser = subparsers.add_parser("add", help="Add Document(s)")
add_parser.add_argument("-f", "--file", help="File path or name for HTML file")
add_parser.add_argument("-u", "--url", help="URL string for the document")

args = parser.parse_args()

if args.command == "list":
    # fetch_reader_document_list_api()
    print("Fetching Document list...")
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
