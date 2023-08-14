"""Functions for handling bookmarks, loading and saving reading lists, and managing HTML files."""
from json import JSONEncoder, dumps, loads
from collections import namedtuple
from datetime import datetime
from typing import List
from pathlib import Path

from xdg_base_dirs import xdg_data_home
from bs4 import BeautifulSoup

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


def data_directory() -> Path:
    """Returns the data directory for storing reading lists.

    Returns:
        Path: The path to the data directory.
    """
    (target_directory := xdg_data_home() / "reader" / "reading_lists").mkdir(
        parents=True, exist_ok=True
    )
    return target_directory


def reading_list_file() -> Path:
    """Returns the path to the reading list JSON file.

    Returns:
        Path: The path to the reading list JSON file.
    """
    return data_directory() / "chrome.json"


def save_reading_list(reading_list: list[Bookmark]) -> None:
    """Loads the reading list from a JSON file or builds it from an HTML file.

    Args:
        file_path (str, optional): The path to the HTML file. Defaults to None.

    Returns:
        List[Bookmark]: The loaded list of bookmarks.
    """
    reading_list_file().write_text(dumps(reading_list, indent=4, sort_keys=True))


def load_reading_list(file_path: str = None) -> List[Bookmark]:
    return (
        [
            Bookmark(title, location, add_date)
            for (title, location, add_date) in loads(reading_list.read_text())
        ]
        if (reading_list := reading_list_file()).exists()
        else build_reading_list(file_path)
    )


def build_html_path(file_path: str = None) -> Path:
    """Builds the path to an HTML file, either using a custom file_path or the default.

    Args:
        file_path (str, optional): The path to the HTML file. Defaults to None.

    Returns:
        Path: The path to the HTML file.
    """
    default_folder = Path.home() / "Downloads"

    if file_path:
        html_path = Path(file_path)
        if not html_path.is_absolute():  # Check if provided file_path is a valid path
            html_path = default_folder / html_path
    else:
        html_path = default_folder / CHROME_DEFAULT_FILENAME

    html_path = html_path.with_suffix(".html")

    return html_path


def build_reading_list(file_path: str = None) -> None:
    """Builds the reading list from an HTML file and saves it as JSON.

    Args:
        file_path (str, optional): The path to the HTML file. Defaults to None.
    """
    file_path = build_html_path(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    reading_list = [
        Bookmark(
            link.text,
            link.get("href"),
            utcfromtimestamp_in_microseconds(float(link.get("add_date"))),
        )
        for link in soup.find_all("a")
    ]

    save_reading_list(reading_list)


if __name__ == "__main__":
    # Example usage
    file_path = "/path/to/CustomReadingList"
    file_path = None
    file_path = "CustomReadingList"
    file_path = "/Users/scott_carvalho/projects/reader-import/ReadingList.html"

    # load reading list
    reading_list = load_reading_list(file_path)
