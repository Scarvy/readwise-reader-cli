import pytest

from readercli.api import validate_token


def test_validate_token_invalid():
    token = "invalid_token"
    result = validate_token(token)
    assert result is False
