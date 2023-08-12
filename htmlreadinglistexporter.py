from json import JSONEncoder, dumps, loads
from collections import namedtuple
from datetime import datetime
from typing import Any, List
from pathlib import Path

from xdg_base_dirs import xdg_data_home
from bs4 import BeautifulSoup

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
CHROME_DEFAULT_FILENAME = "ReadingList"

Bookmark = namedtuple("Bookmark", "title url add_date")


class BookmarkEncoder(JSONEncoder):
    def default(self, o: object) -> Any:
        return str(o) if isinstance(o, Path) else o


def utcfromtimestamp_in_microseconds(timestamp_microseconds: float) -> datetime:
    timestamp_seconds = (
        timestamp_microseconds / 1_000_000
    )  # Convert microseconds to seconds

    datetime_obj = datetime.utcfromtimestamp(timestamp_seconds)

    return datetime_obj.strftime(DATETIME_FORMAT)


def data_directory() -> Path:
    (target_directory := xdg_data_home() / "reader" / "reading_lists").mkdir(
        parents=True, exist_ok=True
    )
    return target_directory


def reading_list_file() -> Path:
    return data_directory() / "chrome.json"


def save_reading_list(reading_list: list[Bookmark]) -> None:
    reading_list_file().write_text(
        dumps(reading_list, indent=4, sort_keys=True, cls=BookmarkEncoder)
    )


def load_reading_list(file_path: str = None) -> List[Bookmark]:
    return (
        [
            Bookmark(title, Path(location), add_date)
            for (title, location, add_date) in loads(reading_list.read_text())
        ]
        if (reading_list := reading_list_file()).exists()
        else build_reading_list(file_path)
    )


def build_html_path(file_path: str = None) -> Path:
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

    html_path = build_html_path(file_path)
    print("HTML Path:", html_path)

    # load reading list
    reading_list = load_reading_list(html_path)
