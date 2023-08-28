import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from readercli.utils import (
    utcfromtimestamp_in_microseconds,
    is_valid_url,
    build_reading_list,
    count_category_values,
    batch_add_documents,
)


@pytest.mark.parametrize(
    "timestamp_microseconds, expected_result",
    [
        (1630000000000, "2021-08-27 20:26:40"),
        # Add more test cases if needed
    ],
)
def test_utcfromtimestamp_in_microseconds(timestamp_microseconds, expected_result):
    result = utcfromtimestamp_in_microseconds(timestamp_microseconds)
    assert result == expected_result


def test_is_valid_url_valid():
    url = "https://www.example.com"
    result = is_valid_url(url)
    assert result is True


def test_is_valid_url_invalid():
    url = "invalid_url"
    result = is_valid_url(url)
    assert result is False


class MockAPIHandler:
    def add_document(self, data):
        if "error" in data["url"]:
            return 500
        elif "exists" in data["url"]:
            return 200
        else:
            return 201


@patch("your_module.APIHandler", MockAPIHandler)
def test_batch_add_documents():
    documents = [
        MagicMock(url="https://www.example.com/add"),
        MagicMock(url="https://www.example.com/exists"),
        MagicMock(url="https://www.example.com/error"),
    ]

    with patch("builtins.print") as mock_print:
        batch_add_documents(documents)

        assert mock_print.call_count == 1  # Check if print_report is called
