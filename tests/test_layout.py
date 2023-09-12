import pytest
from readercli.layout import (
    format_reading_progress,
    format_published_date,
)


@pytest.mark.parametrize("progress, expected", [(0.035575772085228635, "3.56%")])
def test_format_reading_progress(progress, expected):
    assert format_reading_progress(progress) == expected


@pytest.mark.parametrize(
    "timestamp_milliseconds, expected",
    [(1690416000000.0, "2023-07-26")],
)
def test_format_published_date(timestamp_milliseconds, expected):
    assert format_published_date(timestamp_milliseconds) == expected
