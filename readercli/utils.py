from .api import add_document
from .constants import VALID_CATEGORY_OPTIONS


def count_category_values(documents: list[dict]) -> None:
    category_counts = {category: 0 for category in VALID_CATEGORY_OPTIONS}

    for item in documents:
        category = item.get("category")
        if category in category_counts:
            category_counts[category] += 1

    return category_counts


def add_document_batch(documents: list[dict]) -> None:
    for document in documents:
        add_document(data={"url": document.url})
