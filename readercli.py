import argparse

# from api import fetch_reader_document_list_api, add_document

parser = argparse.ArgumentParser(
    description="Save or List Documents from Readwise Reader",
)
parser.add_argument("-l", "--list", action="store_true", help="List Document(s)")
parser.add_argument("-a", "--add", action="store_true", help="Add Document(s)")

args = parser.parse_args()

if args.list:
    # fetch_reader_document_list_api()
    print("Fetching Document list...")
elif args.add:
    # add_document()
    print("Adding Document(s)...")
else:
    parser.print_help()
