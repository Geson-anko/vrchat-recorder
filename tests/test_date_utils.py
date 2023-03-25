import pytest
from freezegun import freeze_time

from vrchat_recorder import date_utils as mod


@pytest.mark.parametrize(
    "format, expected_output",
    [
        ("%Y-%m-%d-%H-%M-%S-%f", "2023-04-01-12-30-00-000000"),
        ("%Y-%m-%d", "2023-04-01"),
        ("%H:%M:%S", "12:30:00"),
    ],
)
def test_get_now_str(format: str, expected_output: str) -> None:
    with freeze_time("2023-04-01 12:30:00"):
        result = mod.get_now_str(format)
        assert result == expected_output
