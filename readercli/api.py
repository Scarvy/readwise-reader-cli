"""Provides code to fetch and manage document information."""
import logging
import os
import time
from functools import wraps
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

HTTP_CODE_HANDLING = {
    200: "valid",
    201: "valid",
    204: "valid",
    401: "invalid",
    429: "retry",
}


def build_log_message(func, *args, **kwargs):
    if func.__name__ == "list_documents":
        request_type = "GET"
        category = kwargs.get("category")
        location = kwargs.get("location")
        updated_after = kwargs.get("updated_after")
        msg = f"Making {request_type} request - parameters: category {category} location {location} updated-after {updated_after}"
    elif func.__name__ == "add_document":
        request_type = "POST"
        doc_info = kwargs.get("doc_info")
        url = doc_info.url
        msg = f"Making {request_type} request - document info: URL {str(url)}"
    elif func.__name__ == "validate_token":
        request_type = "GET"
        token = kwargs.get("token")
        msg = f"Making {request_type} request - Token: {token}"
    else:
        request_type = "Unknown"
        msg = f"Making {request_type} request"
    return msg


def log(func):
    @wraps(func)
    def logger(*args, **kwargs):
        debug = kwargs.pop("debug", False)
        if debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            logger = logging.getLogger(__name__)

            msg = build_log_message(func, *args, **kwargs)

            logger.debug(msg)

        result = func(*args, **kwargs)

        return result

    return logger


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


@log
def list_documents(
    id: Optional[str] = None,
    category: Optional[CategoryEnum] = None,
    location: Optional[LocationEnum] = None,
    updated_after: Optional[datetime] = None,
    debug: bool = False,
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


@log
def add_document(doc_info: DocumentInfo, debug: bool = False) -> Response:
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


@log
def validate_token(token: str, debug: bool = False) -> bool:
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
