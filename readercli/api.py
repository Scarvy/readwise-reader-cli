"""Provides code to fetch and manage document information."""
import os
import time
import logging
from typing import List

import datetime
import requests
from requests.adapters import HTTPAdapter
import urllib3

import dotenv
from click import secho

urllib3.disable_warnings()
dotenv.load_dotenv()

_TOKEN_URL = "https://readwise.io/access_token"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class APIHandler:
    """A class to handle requests to the Reader API."""

    HTTP_CODE_HANDLING = {
        "204": "valid",
        "401": "invalid",
        "429": "retry",
        "500": "invalid",
    }

    def __init__(self, token=None):
        if token is None:
            token = os.getenv("READER_API_TOKEN")
        else:
            raise ValueError("API token not provided.")

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {token}"})
        self.session.mount(
            "https://", HTTPAdapter(pool_connections=10, pool_maxsize=10)
        )

    @classmethod
    def validate_token(self, token: str) -> bool:
        """Check that a token is valid."""

        response = requests.get(
            "https://readwise.io/api/v2/auth/",
            headers={"Authorization": f"Token {token}"},
        )
        handling_code = self.HTTP_CODE_HANDLING[str(response.status_code)]
        if not handling_code == "valid":
            secho(f"Invalid token - check your token at {_TOKEN_URL}", fg="bright_red")
            return False
        return True

    def fetch_documents(
        self,
        updated_after: datetime.datetime = None,
        location: str = None,
        category: str = None,
    ) -> List[dict] | List:
        """Fetches documents from the Readwise Reader API.

        Args:
            updated_after datetime: Update after datetime object.
            location (str, optional): The location to filter documents by.
            category (str, optional): The category to filter documents by.

        Returns:
            List[dict] | List: A list of dictionaries containing document information.
        """

        full_data = []
        next_page_cursor = None

        updated_after = updated_after.isoformat() if updated_after else updated_after

        while True:
            # construct parameters
            params = {
                "pageCursor": next_page_cursor,
                "updateAfter": updated_after,
                "location": location,
                "category": category,
            }

            logger.info("Fetch: %s ...", params)

            response = self.session.get(
                url="https://readwise.io/api/v3/list/",
                params=params,
                verify=False,
            )

            if not response.status_code == 200:
                handling_code = self.HTTP_CODE_HANDLING[str(response.status_code)]

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
                    secho(
                        f"Unknown response code {response.status_code}", fg="bright_red"
                    )
                    break

            full_data.extend(response.json()["results"])
            next_page_cursor = response.json().get("nextPageCursor")

            if not next_page_cursor:
                break

        return full_data

    def add_document(self, data: dict) -> int:
        """Adds a document to a users Reader account.

        Args:
            data (dict): The data of the document to be added.
        """

        while True:
            response = self.session.post(
                url="https://readwise.io/api/v3/save/", json=data
            )

            if not response.status_code in (201, 200):
                handling_code = self.HTTP_CODE_HANDLING[str(response.status_code)]

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
                    secho(
                        f"Unknown response code {response.status_code}", fg="bright_red"
                    )
                    break

            else:
                break

        return response.status_code
