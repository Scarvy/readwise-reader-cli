"""Provides code to fetch and manage document information."""
import os
import time
import logging
from typing import List

import datetime
import requests
import urllib3

import dotenv
from click import secho

urllib3.disable_warnings()
dotenv.load_dotenv()


_TOKEN_URL = "https://readwise.io/access_token"

_BASE_URL = "https://readwise.io/api/v3/"
_AUTH_TOKEN_ENDPOINT = "https://readwise.io/api/v2/auth/"
_LIST_ENDPOINT = "list"
_CREATE_ENDPOINT = "save"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


HTTP_CODE_HANDLING = {
    "204": "valid",
    "401": "invalid",
    "429": "retry",
    "500": "invalid",
}


def validate_token(token: str) -> bool:
    """Check that a token is valid."""

    response = requests.get(
        _AUTH_TOKEN_ENDPOINT,
        headers={"Authorization": f"Token {token}"},
    )
    handling_code = HTTP_CODE_HANDLING[str(response.status_code)]
    if not handling_code == "valid":
        secho(f"Invalid token - check your token at {_TOKEN_URL}", fg="bright_red")
        return False
    return True


def fetch_documents(
    id: str = None,
    updated_after: datetime.datetime = None,
    location: str = None,
    category: str = None,
) -> List[dict] | List:
    """Fetches documents from the Readwise Reader API.

    Args:
        id (str, optional): document unique identifier
        updated_after (datetime, optional): Update after datetime object.
        location (str, optional): The location to filter documents by.
        category (str, optional): The category to filter documents by.

    Returns:
        List[dict] | List: A list of dictionaries containing document information.
    """
    full_data = []

    params = {
        "id": id,
        "updatedAfter": updated_after,
        "location": location,
        "category": category,
    }
    next_page_cursor = None

    while True:
        if next_page_cursor:
            params["pageCursor"] = next_page_cursor

        logger.info("Fetch: %s ...", params)

        response = requests.get(
            url=f"{_BASE_URL}{_LIST_ENDPOINT}",
            params=params,
            headers={"Authorization": f"Token {os.getenv('READER_API_TOKEN')}"},
            verify=False,
        )

        if not response.status_code == 200:
            handling_code = HTTP_CODE_HANDLING[str(response.status_code)]

            if handling_code == "retry":
                retry_after = int(
                    response.headers.get("Retry-After", 5)
                )  # Default to 5 seconds if no Retry-After header
                secho(
                    f"Too many requests. Retring in {retry_after} seconds...",
                    fg="bright_yellow",
                )
                time.sleep(retry_after)
                continue

            else:
                secho(f"Unknown response code {response.status_code}", fg="bright_red")
                break

        results = response.json().get("results")

        if results:
            full_data.extend(results)

        next_page_cursor = response.json().get("nextPageCursor")

        if not next_page_cursor:
            break

    return full_data


def add_document(metadata: dict) -> int:
    """Adds a document to a users Reader account.

    Args:
        metadata (dict): Metadata about a specific document to be added.
    """
    while True:
        response = requests.post(
            url=f"{_BASE_URL}{_CREATE_ENDPOINT}",
            headers={"Authorization": f"Token {os.getenv('READER_API_TOKEN')}"},
            json=metadata,
        )

        if not response.status_code in (201, 200):
            handling_code = HTTP_CODE_HANDLING[str(response.status_code)]

            if handling_code == "retry":
                retry_after = int(
                    response.headers.get("Retry-After", 5)
                )  # Default to 5 seconds if no Retry-After header
                secho(
                    f"Too many requests. Retring in {retry_after} seconds...",
                    fg="bright_yellow",
                )
                time.sleep(retry_after)
                continue

            else:
                secho(f"Unknown response code {response.status_code}", fg="bright_red")
                break

        else:
            break

    return response
