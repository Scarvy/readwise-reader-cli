"""Provides code to fetch and manage document information."""
import os
import time
from typing import List, Optional, Union

import datetime
import requests
import urllib3
import dotenv

urllib3.disable_warnings()
dotenv.load_dotenv()


def _convert_after_days(days: int = None) -> str:
    return (
        datetime.datetime.now()
        - datetime.timedelta(days=((days := days) if days else 1))
    ).isoformat()


def fetch_documents(
    updated_after: Optional[Union[str, int]] = None,
    location: str = None,
    category: str = None,
) -> List[dict] | List:
    """Fetches documents from the Readwise Reader API.

    Args:
        updated_after (str, int, optional): The date after which to fetch updated documents or N number of days.
        location (str, optional): The location to filter documents by.
        category (str, optional): The category to filter documents by.

    Returns:
        List[dict] | List: A list of dictionaries containing document information.
    """
    full_data = []
    next_page_cursor = None
    while True:
        params = {}
        if next_page_cursor:
            params["pageCursor"] = next_page_cursor
        if updated_after:
            if isinstance(updated_after, int):
                updated_after = _convert_after_days(updated_after)
            params["updatedAfter"] = updated_after
        if location:
            params["location"] = location
        if category:
            params["category"] = category
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


def add_document(data: dict) -> None:
    """Adds a document to Readwise using the Reader API.

    Args:
        data (dict): The data of the document to be added.
    """
    response = requests.post(
        url="https://readwise.io/api/v3/save/",
        headers={"Authorization": f"Token {os.getenv('READER_API_TOKEN')}"},
        json=data,
    )

    if response.status_code == 201:
        print("Document added successfully!")
    elif response.status_code == 200:
        print("Document already exist.")
    elif response.status_code == 401:
        print("Failed to add document. Please provide a valid API key.")
    elif response.status_code == 500:
        print("An error occurred while adding the document. Please try again later.")
    else:
        print(f"Unexpected response: {response.status_code}")

    return response
