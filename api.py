import os
import time
from typing import List

import datetime
import requests
import urllib3
import dotenv

urllib3.disable_warnings()
dotenv.load_dotenv()


def fetch_reader_document_list_api(
    updated_after=None, location=None
) -> List[dict] | List:
    full_data = []
    next_page_cursor = None
    while True:
        params = {}
        if next_page_cursor:
            params["pageCursor"] = next_page_cursor
        if updated_after:
            params["updatedAfter"] = updated_after
        if location:
            params["location"] = location
        print("Making export api request with params " + str(params) + "...")
        response = requests.get(
            url="https://readwise.io/api/v3/list/",
            params=params,
            headers={"Authorization": f"Token {os.getenv('READER_API_TOKEN')}"},
            verify=False,
        )

        if response.status_code == 429:
            print("Received a 429 response - Too Many Requests")
            retry_after = int(
                response.headers.get("Retry-After", 5)
            )  # Default to 5 seconds if no Retry-After header
            print(f"Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            response = requests.get(
                url="https://readwise.io/api/v3/list/",
                params=params,
                headers={"Authorization": f"Token {os.getenv('READER_API_TOKEN')}"},
                verify=False,
            )

        full_data.extend(response.json()["results"])
        next_page_cursor = response.json().get("nextPageCursor")
        if not next_page_cursor:
            break
    return full_data


if __name__ == "__main__":
    """List Documents from Reader API"""
    # Get all of a user's documents from all time
    all_data = fetch_reader_document_list_api()

    # Get all of a user's archived documents
    archived_data = fetch_reader_document_list_api(location="archive")

    # Later, if you want to get new documents updated after some date, do this:
    docs_after_date = datetime.datetime.now() - datetime.timedelta(
        days=1
    )  # use your own stored date
    new_data = fetch_reader_document_list_api(docs_after_date.isoformat())
