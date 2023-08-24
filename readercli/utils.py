"""Utility functions."""

from datetime import datetime
from collections import namedtuple
from bs4 import BeautifulSoup

from .api import add_document
from .constants import VALID_CATEGORY_OPTIONS

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
CHROME_DEFAULT_FILENAME = "ReadingList"

# A named tuple to represent bookmarks with title, URL, and add_date
Bookmark = namedtuple("Bookmark", "title url add_date")


def utcfromtimestamp_in_microseconds(timestamp_microseconds: float) -> datetime:
    """Converts a timestamp in microseconds to a UTC datetime object.

    Args:
        timestamp_microseconds (float): The timestamp in microseconds.

    Returns:
        datetime: A UTC datetime object.
    """
    timestamp_seconds = (
        timestamp_microseconds / 1_000_000
    )  # Convert microseconds to seconds

    datetime_obj = datetime.utcfromtimestamp(timestamp_seconds)

    return datetime_obj.strftime(DATETIME_FORMAT)


def build_reading_list(file_bytes: bytes) -> list[Bookmark]:
    """Build reading list from html file.

    Args:
        file_bytes (bytes): bytes from file

    Returns:
        reading_list (list[dict]): A list of `Bookmark`s
    """
    soup = BeautifulSoup(file_bytes, "html.parser")

    reading_list = [
        Bookmark(
            link.text,
            link.get("href"),
            utcfromtimestamp_in_microseconds(float(link.get("add_date"))),
        )
        for link in soup.find_all("a")
    ]

    return reading_list


def count_category_values(documents: list[dict]) -> dict:
    """Category counts

    Args:
        documents (list[dict]): A list of `Bookmark`s

    Returns:
        category_counts dict: a dictionary of category counts
    """
    category_counts = {category: 0 for category in VALID_CATEGORY_OPTIONS}

    for item in documents:
        category = item.get("category")
        if category in category_counts:
            category_counts[category] += 1

    return category_counts


def add_document_batch(documents: list[dict]) -> None:
    """Batch documents to add to Reader Library.

    Args:
        documents (list[dict]): A list of `Bookmark`s
    """

    for document in documents:
        add_document(data={"url": document.url})
