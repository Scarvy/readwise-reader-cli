import pytest
from unittest import mock

from readercli.api import validate_token, _get_list, _create_doc


def mock_request_get(**kwargs):
    class MockGetResponse:
        def __init__(self, count, next_page_cursor, json_data):
            self.count = count
            self.next_page_cursor = next_page_cursor
            self.results = [json_data]

        def count(self):
            return self.count

        def next_page_cursor(self):
            return self.next_page_cursor

        def resutls(self):
            return self.results

    if kwargs["params"]["location"] == "new":
        return MockGetResponse(2304, "01gm6kjzabcd609yepjrmcgz8a", {"location": "new"})
    if kwargs["params"]["location"] == "later":
        return MockGetResponse(
            2304, "01gm6kjzabcd609yepjrmcgz8a", {"location": "later"}
        )

    return MockGetResponse(None, None, None)


@mock.patch("requests.get", side_effect=mock_request_get, autospec=True)
def test_get_list_new_location(_):
    _get_list({"location": "new"})


@mock.patch("requests.get", side_effect=mock_request_get, autospec=True)
def test_get_list_later_location(_):
    _get_list({"location": "later"})


def mock_request_post(**kwargs):
    class MockPostResponse:
        def __init__(self, _id, url):
            self.id = _id
            self.url = url

        def _id(self):
            return self.id

        def url(self):
            return self.url

    if kwargs["json"]["url"] == "https://new_article.com":
        return MockPostResponse(
            "0000ffff2222eeee3333dddd4444",
            "https://read.readwise.io/new/read/0000ffff2222eeee3333dddd4444",
        )

    if kwargs["json"]["url"] == "https://new_article.com":
        return MockPostResponse(
            "0000ffff2222eeee3333dddd4444",
            "https://read.readwise.io/new/read/0000ffff2222eeee3333dddd4444",
        )

    return MockPostResponse(None, 404)


@mock.patch("requests.post", side_effect=mock_request_post, autospec=True)
def test_create_new_document(_):
    _create_doc(info={"url": "https://new_article.com"})


@mock.patch("requests.post", side_effect=mock_request_post, autospec=True)
def test_create_already_exist_document(_):
    _create_doc(info={"url": "https://already_exist_article.com"})


def test_validate_token_invalid():
    token = "invalid_token"
    result = validate_token(token)
    assert result is False
