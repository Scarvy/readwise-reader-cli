import pytest
from readercli.api import (
    APIHandler,
)


@pytest.fixture
def api_handler():
    return APIHandler()


def test_validate_token_invalid(api_handler):
    token = "invalid_token"
    result = api_handler.validate_token(token)
    assert result is False


def test_fetch_documents(api_handler):
    pass


def test_add_document(api_handler):
    pass
