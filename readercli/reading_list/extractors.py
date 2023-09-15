import csv
from abc import ABC, abstractmethod
from typing import Any, List

from bs4 import BeautifulSoup

from ..models import DocumentInfo


class ReadingListExtractor(ABC):
    """Abstract class for ReadingListExtractors"""

    @abstractmethod
    def extract_document_info(self, input_file: str) -> List[DocumentInfo]:
        pass


class HTMLReadingListExtractor(ReadingListExtractor):
    """
    Extract document information from html file

    Example:
    html
        <TITLE>Reading List</TITLE>
        <H1>Reading List</H1>
            <DL><p>
                <DT><A HREF="https://www.example.com" ADD_DATE="1679670930960538">Example Title</A>
            </DL><p>
    """

    def extract_document_info(self, input_file: str) -> List[DocumentInfo]:
        documents = []

        with open(input_file, "r") as f:
            content = f.read()

            soup = BeautifulSoup(content, "html.parser")

            for link in soup.find_all("a"):
                url = link.get("href")
                title = link.get_text()

                document = DocumentInfo(title=title, url=url)
                documents.append(document)

        return documents


class CSVReadingListExtractor(ReadingListExtractor):
    """
    Extract document information from CSV file

    Example:
        csv
            URL,Title,
            https://www.example.com,Example Domain
    """

    def extract_document_info(self, input_file: str) -> List[DocumentInfo]:
        documents = []

        with open(input_file, "r") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header row

            for row in reader:
                url: Any = row[0]
                title = row[1] if len(row) >= 2 else None

                document = DocumentInfo(title=title, url=url)
                documents.append(document)

        return documents


def create_extractor(file_type: str) -> ReadingListExtractor:
    extractor_map = {"html": HTMLReadingListExtractor, "csv": CSVReadingListExtractor}
    if file_type not in extractor_map:
        raise ValueError(f"Invalid file type: {file_type}")
    return extractor_map[file_type]()


def build_reading_list(input_file: str, file_type: str) -> List[DocumentInfo]:
    """Builds a reading list from a given file.

    Args:
        input_file (str): a file path
        file_type (str): file type (ex. .csv)

    Raises:
        ValueError: If file type is not supported

    Returns:
        List[DocumentInfo]: A list of `DocumentInfo` objects
    """
    extractor = create_extractor(file_type)

    return extractor.extract_document_info(input_file)
