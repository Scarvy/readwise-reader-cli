import pytest
from unittest import mock

from readercli.api import validate_token, _get_list, _create_doc


# source https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response
def mock_request_get(**kwargs):
    class MockGetResponse:
        def __init__(self, status_code, count, next_page_cursor, results):
            self.status_code = status_code
            self.json = [
                {"count": count, "nextPageCursor": next_page_cursor, "results": results}
            ]

        def status_code(self):
            return self.status_code

        def resutls(self):
            return self.results

    location = kwargs.get("location")

    if location:
        return MockGetResponse(
            200, 2304, "01gm6kjzabcd609yepjrmcgz8a", {"key1": "value1"}
        )

    return MockGetResponse(200, 0, None, None)


@mock.patch("requests.get", side_effect=mock_request_get, autospec=True)
def test_get_list(_):
    _get_list(params={"location": "new"})


@mock.patch("requests.get", side_effect=mock_request_get, autospec=True)
def test_get_list_empty(_):
    _get_list(params={"location": None})


def mock_request_post(**kwargs):
    class MockPostResponse:
        def __init__(self, json_data, status_code):
            self.json = json_data
            self.status_code = status_code

        def json(self):
            return self.json

        def status_code(self):
            return self.status_code

    if kwargs["json"]["url"] == "https://new_article.com":
        return MockPostResponse(
            {"key1", "value1"},
            201,
        )

    if kwargs["json"]["url"] == "https://already_exist_article.com":
        return MockPostResponse(
            {"key1", "value1"},
            200,
        )

    if kwargs["json"]["url"] == "bad_article_url":
        return MockPostResponse({"key1": "value1"}, 400)

    return MockPostResponse(None, 400)


@mock.patch("requests.post", side_effect=mock_request_post, autospec=True)
def test_create_new_document(_):
    _create_doc(info={"url": "https://new_article.com"})


@mock.patch("requests.post", side_effect=mock_request_post, autospec=True)
def test_create_already_exist_document(_):
    _create_doc(info={"url": "https://already_exist_article.com"})


@mock.patch("requests.post", side_effect=mock_request_post, autospec=True)
def test_create_invalid_url_document(_):
    _create_doc(info={"url": "bad_article_url"})


def test_validate_token_invalid():
    token = "invalid_token"
    result = validate_token(token)
    assert result is False
