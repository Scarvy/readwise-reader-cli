"""Utility functions."""
from datetime import datetime, timedelta
from typing import List, Dict, Union, Any

from click import secho
from rich.progress import Progress

from .api import add_document
from .constants import VALID_CATEGORY_OPTIONS, VALID_LOCATION_OPTIONS
from .models import DocumentInfo

DATE_RANGE_MAP = {"today": {"days": 1}, "week": {"weeks": 1}, "month": {"days": 30}}


def convert_date_range(date_range: str) -> datetime:
    return datetime.now() - timedelta(**DATE_RANGE_MAP[date_range])


def count_category_values(documents: List[DocumentInfo]) -> Dict[str, int]:
    category_counts = {category: 0 for category in VALID_CATEGORY_OPTIONS}

    for doc in documents:
        doc_ctgry = doc.model_dump(include={"category"})
        category = doc_ctgry.get("category")
        if category:
            if category in category_counts:
                category_counts[category] += 1

    return category_counts


def count_location_values(documents: List[DocumentInfo]) -> Dict[str, int]:
    location_counts = {location: 0 for location in VALID_LOCATION_OPTIONS}

    for document in documents:
        document_loc = document.model_dump(include={"location"})
        location = document_loc.get("location")
        if location:
            if location in location_counts:
                location_counts[location] += 1

    return location_counts


def count_tag_values(documents: List[DocumentInfo]) -> Dict[str, int]:
    tag_counts: Dict[str, int] = {}

    for doc in documents:
        doc_tags = doc.model_dump(include=["tags"])
        tags = doc_tags.get("tags")
        if tags:
            for tag_name, _ in tags.items():
                if tag_name in tag_counts:
                    tag_counts[tag_name] += 1
                else:
                    tag_counts[tag_name] = 1

    sorted_tag_counts = dict(
        sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)
    )

    return sorted_tag_counts


def print_report(adds: int, exists: int, failures: int, total: int) -> None:
    secho("Report:")
    secho(f"Additions: {adds} out of {total}", fg="bright_green")
    secho(f"Already Exists: {exists}", fg="bright_yellow")
    secho(f"Failures: {failures}", fg="bright_red")


def batch_add_documents(documents: List[DocumentInfo], debug=False) -> None:
    """Batch documents to add to Reader Library.

    Args:
        documents (List[DocumentInfo]): A list of `DocumentInfo` objects
    """
    number_of_documents = len(documents)

    # track counts
    adds = 0
    exists = 0
    failures = 0

    with Progress() as progress:
        task = progress.add_task("Uploading...", total=number_of_documents)

        for document in documents:
            response = add_document(doc_info=document, debug=debug)

            if response.status_code == 201:
                adds += 1
                progress.update(task, advance=1, description="Success")
            elif response.status_code == 200:
                adds += 1
                exists += 1
                progress.update(task, advance=1, description="Already Exists")
            else:
                failures += 1
                progress.update(task, advance=1, description="Failure")

    print_report(adds, exists, failures, number_of_documents)
