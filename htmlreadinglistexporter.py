import json
from collections import namedtuple
from datetime import datetime
from typing import List
from pathlib import Path

from bs4 import BeautifulSoup

from document import DocumentInfo

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

Bookmark = namedtuple("Bookmark", "title url add_date")


def utcfromtimestamp_in_microseconds(timestamp_microseconds: float) -> datetime:
    timestamp_seconds = (
        timestamp_microseconds / 1_000_000
    )  # Convert microseconds to seconds

    datetime_obj = datetime.utcfromtimestamp(timestamp_seconds)

    return datetime_obj.strftime(DATETIME_FORMAT)


def build_chrome_reading_list(file_path: str) -> List[Bookmark]:
    if file_path.endswith(".html"):
        with open(file_path, "r") as file:
            html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    chrome_reading_list = [
        Bookmark(
            link.text,
            link.get("href"),
            utcfromtimestamp_in_microseconds(float(link.get("add_date"))),
        )
        for link in soup.find_all("a")
    ]

    return chrome_reading_list


def to_json(data: List[Bookmark]) -> None:
    with open("chrome_reading_list.json", "w") as f:
        json.dump(data, f, indent=4)


def reading_list_to_json(file_path: str) -> None:
    chrome_reading_list = build_chrome_reading_list(file_path=file_path)

    to_json(chrome_reading_list)


def get_reading_list() -> List[DocumentInfo]:
    document_list = []

    with open("chrome_reading_list.json", "r") as f:
        chrome_reading_list = json.load(f)
        for bookmark in chrome_reading_list:
            url = bookmark[1]  # bookmark url
            document_list.append(DocumentInfo(url, tags=["chrome-reading-list"]))
    return document_list


if __name__ == "__main__":
    file_path = "ReadingList.html"

    reading_list_to_json(file_path=file_path)

    chrome_reading_list = get_reading_list()
