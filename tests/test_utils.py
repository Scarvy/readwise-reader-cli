import pytest

from datetime import datetime, timedelta

from readercli.utils import convert_date_range


@pytest.fixture(
    params=[
        ("today", timedelta(days=1)),
        ("week", timedelta(weeks=1)),
        ("month", timedelta(days=30)),
    ]
)
def date_range_fixture(request):
    return request.param


def test_convert_date_range(date_range_fixture):
    date_range_option, expected_timedelta = date_range_fixture
    expected_date = datetime.now() - expected_timedelta
    actual_date = convert_date_range(date_range_option)
    assert abs((expected_date - actual_date).total_seconds()) < 1
