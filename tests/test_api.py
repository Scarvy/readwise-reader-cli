import pytest
from unittest import mock

from readercli.api import validate_token, _fetch_results


def mock_request_get(**kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs["location"] == "new":
        return MockResponse({"location": "new"})
    elif kwargs["location"] == "later":
        return MockResponse({"location": "later"}, 200)

    return MockResponse(None, 404)


@mock.patch("requests.get", side_effect=mock_request_get, autospec=True)
def test_fetch_results(_):
    _fetch_results(params={"location": "new"})


def test_validate_token_invalid():
    token = "invalid_token"
    result = validate_token(token)
    assert result is False
