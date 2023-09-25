from unittest.mock import Mock, patch

import pytest

from readercli.api import _fetch_results  # list_documents,
from readercli.api import (
    _create_doc,
    _get_list,
    _handle_http_status,
    add_document,
    doc_info_jsonify,
    list_parameter_jsonify,
    validate_token,
)
from readercli.models import DocumentInfo


def test_list_parameter_jsonify():
    mock_params = Mock()
    mock_params.model_dump.return_value = {"key": "value"}
    assert list_parameter_jsonify(mock_params) == {"key": "value"}


def test_doc_info_jsonify():
    mock_doc_info = Mock()
    mock_doc_info.model_dump.return_value = {"key": "value"}
    assert doc_info_jsonify(mock_doc_info) == {"key": "value"}


@patch("readercli.api.requests.get")
def test__get_list(mock_get):
    mock_get.return_value = {"key1": "value1", "key2": [{"key1": "value1"}]}
    assert _get_list({"key": "value"}) == {
        "key1": "value1",
        "key2": [{"key1": "value1"}],
    }


@patch("readercli.api.requests.post")
def test__create_doc(mock_post):
    mock_post.return_value = {"key1": "value1"}
    assert _create_doc({"key": "value"}) == {"key1": "value1"}


def test__handle_http_status():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers.get.return_value = 5
    assert _handle_http_status(mock_response) == ("valid", 5)


@patch("readercli.api._get_list")
@patch("readercli.api._handle_http_status")
def test__fetch_results(mock_handle_status, mock_get_list):
    mock_handle_status.return_value = ("valid", 5)
    mock_get_list.return_value = Mock(
        json=lambda: {"results": [], "nextPageCursor": None}
    )
    assert list(_fetch_results({"key": "value"})) == [[]]


# @patch("readercli.api.list_documents")
# def test_list_documents(mock_fetch_results):
#     mock_fetch_results.return_value = [
#         DocumentInfo(**{"url": "https://www.example.com"})
#     ]
#     assert list_documents() == [DocumentInfo(**{"url": "https://www.example.com"})]


@patch("readercli.api._create_doc")
@patch("readercli.api._handle_http_status")
def test_add_document(mock_handle_status, mock_create_doc):
    mock_handle_status.return_value = ("valid", 5)
    mock_create_doc.return_value = "response"
    assert add_document(Mock()) == "response"


@patch("readercli.api.requests.get")
def test_validate_token(mock_get):
    mock_get.return_value = Mock(status_code=204)
    assert validate_token("token") == True
