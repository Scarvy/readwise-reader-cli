"""A dataclass for storing Document information"""
from json import dumps
from dataclasses import dataclass
from typing import List, Optional
from httpx import URL

from constants import VALID_LOCATION_OPTIONS, VALID_CATEGORY_OPTIONS

# TODO ISSUE add notes property. Won't take empty string "" or None as an argument.


@dataclass()
class DocumentInfo:
    """Represents information about a document.

    Attributes:
        url (URL): The document's unique URL.
        html (str, optional): The document's content in HTML format, or None if it will be scraped from the URL.
            # No html is provided, so the url will be scraped to get the document's content.
        should_clean_html (bool, optional): Whether to clean the HTML content and parse metadata automatically.
        title (str, optional): The document's title.
        author (str, optional): The document's author.
        summary (str, optional): A summary of the document.
        published_date (str, optional): The publication date of the document in ISO 8601 format. Example: "2020-07-14T20:11:24+00:00".
        image_url (str, optional): The URL of a cover image for the document.
        _location (str, optional): The initial state of the document - "new", "later", "archive", or "feed".
        category (str, optional): One of: article, email, rss, highlight, note, pdf, epub, tweet, or video.
        saved_using (str, optional): The source of the document.
        tags (List[str], optional): A list of tags associated with the document. Example: ["tag1", "tag2"].

    Properties:
        location (str): The current location of the document.
        category (str): The category of the document.

    Methods:
        to_dict(): Convert the DocumentInfo instance to a dictionary.
        to_json(): Convert the DocumentInfo instance to json.
    """

    url: URL
    html: Optional[
        str
    ] = None  # No html is provided, so the url will be scraped to get the document's content.
    should_clean_html: Optional[bool] = False
    title: Optional[str] = None
    author: Optional[str] = None
    summary: Optional[str] = None
    published_date: Optional[str] = None
    image_url: Optional[URL] = None
    _location: str = "new"
    _category: str = "article"
    saved_using: Optional[str] = None
    tags: Optional[List[str]] = None

    @property
    def location(self):
        """str: The current location of the document."""
        return self._location

    @location.setter
    def location(self, value):
        if value not in VALID_LOCATION_OPTIONS:
            raise ValueError(f"Invalid location option: {value}")
        self._location = value

    @property
    def category(self):
        """str: The category of the document."""
        return self._category

    @category.setter
    def category(self, value):
        if value is not None and value not in VALID_CATEGORY_OPTIONS:
            raise ValueError(f"Invalid category option: {value}")
        self._category = value

    @property
    def __dict__(self):
        return {
            "url": self.url,
            "html": self.html,
            "should_clean_html": self.should_clean_html,
            "title": self.title,
            "author": self.author,
            "summary": self.summary,
            "published_date": self.published_date,
            "image_url": self.image_url,
            "location": self.location,  # Change the key name
            "category": self.category,
            "saved_using": self.saved_using,
            "tags": self.tags,
        }

    def to_dict(self):
        """Convert the DocumentInfo instance to a dictionary.

        Returns:
            dict: A dictionary containing the attributes of the DocumentInfo instance.

        """
        return self.__dict__

    def to_json(self):
        return dumps(self.__dict__, default=str)


if __name__ == "__main__":
    document_one = DocumentInfo(
        url="https://example.com",
        html="<p>This is the content</p>",
        title="Sample Document",
        tags=["tag1", "tag2"],
    )

    document_one_dict = document_one.to_dict()
    print(document_one_dict)

    document_one_json = document_one.to_json()
    print(document_one_json)

    document_two_dict = {
        "url": "https://realpython.com/python-coding-setup-windows/",
        "title": "Python Coding Setup on Windows",
    }
    document_two = DocumentInfo(**document_two_dict)
    print(document_two.to_dict())
