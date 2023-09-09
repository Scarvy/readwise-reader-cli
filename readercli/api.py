"""Provides code to fetch and manage document information."""
import logging
import os
import time
from datetime import datetime
from typing import List, Optional, Tuple

import dotenv
import requests
import urllib3
from click import secho
from requests import Response

from readercli.constants import (
    AUTH_TOKEN_URL,
    BASE_URL,
    CREATE_ENDPOINT,
    LIST_ENDPOINT,
    TOKEN_URL,
)
from readercli.document import DocumentInfo, ListParameters

urllib3.disable_warnings()
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

HTTP_CODE_HANDLING = {
    200: "valid",
    201: "valid",
    204: "valid",
    401: "invalid",
    429: "retry",
}


def _get_list(params: dict) -> Response:
    resp = requests.get(
        url=f"{BASE_URL}{LIST_ENDPOINT}",
        params=params,
        headers={"Authorization": f"Token {os.getenv('READER_API_TOKEN')}"},
        verify=False,
    )
    return resp


def _handle_http_status(
    resp: Response, retry_after_default: int = 5
) -> Tuple[str, int]:
    handling_code = HTTP_CODE_HANDLING.get(resp.status_code, "unknown")
    retry_after = int(resp.headers.get("Retry-After", retry_after_default))
    return handling_code, retry_after


def list_parameter_json(params: ListParameters) -> dict:
    return params.model_dump(exclude_unset=True, mode="json", by_alias=True)


def _fetch_results(params: dict, retry_after_default: int = 5) -> list[dict]:
    next_page_cursor = None
    while True:
        params["pageCursor"] = next_page_cursor

        logger.info("Fetch: %s ...", params)

        resp = _get_list(params=params)

        handling_code, retry_after = _handle_http_status(resp, retry_after_default)

        if handling_code == "retry":
            time.sleep(retry_after)
            secho(
                f"Too many requests. Retring in {retry_after} seconds...",
                fg="bright_yellow",
            )
        elif handling_code != "valid":
            secho(f"Unknown response code {resp.status_code}", fg="bright_red")
            break

        yield resp.json().get("results", [])

        next_page_cursor = resp.json().get("nextPageCursor")
        if not next_page_cursor:
            break


def list_documents(
    id: Optional[str] = None,
    category: Optional[str] = None,
    location: Optional[str] = None,
    updated_after: Optional[datetime] = None,
) -> List[DocumentInfo]:
    """Fetches a list of `DocumentInfo` objects.

    Args:
        id (str, optional): document unique identifier
        category (str, optional): The category to filter documents by
        location (str, optional): The location to filter documents by
        updated_after (datetime, optional): Update after datetime object

    Returns:
        List[DocumentInfo]: A list of `DocumentInfo` objects
    """

    params = list_parameter_json(
        ListParameters(
            id=id,
            category=category,
            location=location,
            updated_after=updated_after,
        )
    )

    return [
        DocumentInfo(**doc_info)
        for results in _fetch_results(params=params)
        for doc_info in results
    ]


def _create_doc():
    ...


def add_document(metadata: dict) -> int:
    """Adds a document to a users Reader account.

    Args:
        metadata (dict): Metadata about a specific document to be added.
    """
    while True:
        response = requests.post(
            url=f"{BASE_URL}{CREATE_ENDPOINT}",
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

            else:
                secho(f"Unknown response code {response.status_code}", fg="bright_red")
                break

        else:
            break

    return response


def validate_token(token: str) -> bool:
    """Check that a token is valid."""

    response = requests.get(
        AUTH_TOKEN_URL,
        headers={"Authorization": f"Token {token}"},
    )
    handling_code = HTTP_CODE_HANDLING[response.status_code]
    if not handling_code == "valid":
        secho(f"Invalid token - check your token at {TOKEN_URL}", fg="bright_red")
        return False
    return True
