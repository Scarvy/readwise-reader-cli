"""Utility functions."""
import csv
from datetime import datetime
from collections import namedtuple

from click import secho
from rich.progress import Progress
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


def is_valid_url(url: str):
    """Validate URL"""
    return url.startswith("http://") or url.startswith("https://")


def build_reading_list(input_file: str, file_type: str) -> list[Bookmark]:
    """Build reading list from a file.

    Args:
        input_file: file name
        file_type (str): file type

    Returns:
        reading_list (list[dict]): A list of `Bookmark`s
    """
    reading_list = []

    if file_type == "html":
        with open(input_file, "r") as f:
            content = f.read()

            soup = BeautifulSoup(content, "html.parser")

            for link in soup.find_all("a"):
                url = link.get("href")
                if url and is_valid_url(url):
                    title = link.get_text()
                    add_date = utcfromtimestamp_in_microseconds(
                        float(link.get("add_date"))
                    )
                    bookmark = Bookmark(title, url, add_date)
                    reading_list.append(bookmark)
                else:
                    secho(f"URL is invalid. {url}", fg="bright_red")

    elif file_type == "csv":
        with open(input_file, "r") as f:
            reader = csv.reader(f)

            header = next(reader)  # Read the header row

            url_index = header.index("URL") if "URL" in header else None

            if url_index is not None:
                for row in reader:
                    if len(row) >= 1:
                        url = row[0]
                        if url and is_valid_url(url):
                            title = row[1] if len(row) >= 2 else None
                            add_date = row[2] if len(row) >= 3 else None
                            if url:
                                bookmark = Bookmark(title, url, add_date)
                                reading_list.append(bookmark)
                        else:
                            secho(f"URL is invalid. {url}", fg="bright_red")

    else:
        print("Invalid file type.")

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


def print_report(adds, exists, failures, total):
    secho("\nReport:")
    secho(f"Additions: {adds} out of {total}", fg="bright_green")
    secho(f"Already Exists: {exists}", fg="bright_yellow")
    secho(f"Failures: {failures}", fg="bright_red")


def add_document_batch(documents: list[dict]) -> None:
    """Batch documents to add to Reader Library.

    Args:
        documents (list[dict]): A list of `Bookmark`s
    """

    number_of_documents = len(documents)

    # track counts
    adds = 0
    exists = 0
    failures = 0

    with Progress() as progress:
        task = progress.add_task("Uploading...", total=number_of_documents)

        for document in documents:
            status_code = add_document(data={"url": document.url})

            if status_code == 201:
                adds += 1
                progress.update(task, advance=1, description="Success")
            elif status_code == 200:
                adds += 1
                exists += 1
                progress.update(task, advance=1, description="Already Exists")
            else:
                failures += 1
                progress.update(task, advance=1, description="Failure")

    print_report(adds, exists, failures, number_of_documents)
