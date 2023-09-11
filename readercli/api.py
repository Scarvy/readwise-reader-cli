"""Provides code to fetch and manage document information."""
import logging
import os
import time
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Union, Iterable

import dotenv
import requests
import urllib3
from click import secho
from requests import Response

from .constants import (
    AUTH_TOKEN_URL,
    BASE_URL,
    CREATE_ENDPOINT,
    LIST_ENDPOINT,
    TOKEN_URL,
)
from .models import DocumentInfo, ListParameters, CategoryEnum, LocationEnum

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


def list_parameter_jsonify(params: ListParameters) -> Dict[str, Union[str, None]]:
    return params.model_dump(exclude_unset=True, mode="json", by_alias=True)


def doc_info_jsonify(doc_info: DocumentInfo) -> Dict[str, Union[str, None]]:
    return doc_info.model_dump(exclude_unset=True, mode="json")


def _get_list(params: Dict[str, Union[str, None]]) -> Response:
    resp = requests.get(
        url=f"{BASE_URL}{LIST_ENDPOINT}",
        params=params,
        headers={"Authorization": f"Token {os.getenv('READER_API_TOKEN')}"},
        verify=False,
    )
    return resp


def _create_doc(info: Dict[str, Union[str, None]]) -> Response:
    resp = requests.post(
        url=f"{BASE_URL}{CREATE_ENDPOINT}",
        headers={"Authorization": f"Token {os.getenv('READER_API_TOKEN')}"},
        json=info,
    )
    return resp


def _handle_http_status(
    resp: Response, retry_after_default: int = 5
) -> Tuple[str, int]:
    handling_code = HTTP_CODE_HANDLING.get(resp.status_code, "unknown")
    retry_after = int(resp.headers.get("Retry-After", retry_after_default))
    return handling_code, retry_after


def _fetch_results(
    params: Dict[str, Union[str, None]], retry_after_default: int = 5
) -> Iterable[List[dict]]:
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
    category: Optional[CategoryEnum] = None,
    location: Optional[LocationEnum] = None,
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

    params = list_parameter_jsonify(
        ListParameters(
            id=id,
            category=category,
            location=location,
            update_after=updated_after,
            next_page_cursor=None,
        )
    )

    return [
        DocumentInfo(**doc_info)
        for results in _fetch_results(params=params)
        for doc_info in results
    ]


def add_document(doc_info: DocumentInfo) -> Response:
    """Adds a document to a users Reader account.

    Args:
        doc_info (dict): `DocumentInfo` object
    """

    doc_info_json = doc_info_jsonify(doc_info=doc_info)

    while True:
        resp = _create_doc(info=doc_info_json)

        handling_code, retry_after = _handle_http_status(resp=resp)

        if handling_code == "retry":
            time.sleep(retry_after)
            secho(
                f"Too many requests. Retring in {retry_after} seconds...",
                fg="bright_yellow",
            )
        elif handling_code != "valid":
            secho(f"Unknown response code {resp.status_code}", fg="bright_red")
            break

        else:  # If code 200 or 201, break loop
            break

    return resp


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
