import csv
import tempfile
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from vrchat_recorder.data_constants import CSVHeaderNames as HN
from vrchat_recorder.data_constants import get_data_type_name
from vrchat_recorder.gamepad_recorder import GamepadRecorder

temp_dir = tempfile.TemporaryDirectory()
test_dir = Path(temp_dir.name)


def test_gamepad_recorder_init():
    output_file_path = test_dir / "test__init__.csv"
    gpr = GamepadRecorder(output_file_path)
    assert gpr.output_file_path == output_file_path


@pytest.fixture
def sample_event():
    event = MagicMock()
    event.timestamp = 1.23
    event.ev_type = "SampleEventType"
    event.code = "SampleCode"
    event.state = 42
    return event


@pytest.fixture
def sample_event_list(sample_event):
    return [sample_event]


@pytest.fixture
def pytest_mock_gamepad(mocker: MockerFixture):
    return mocker.patch("inputs.get_gamepad")


@pytest.fixture
def gamepad_recorder_with_mocked_methods():
    output_file_path = test_dir / "test.csv"
    gpr = GamepadRecorder(output_file_path)
    gpr._shutdown = False
    return gpr


def test_gamepad_recorder_record(sample_event_list, pytest_mock_gamepad, gamepad_recorder_with_mocked_methods):
    pytest_mock_gamepad.return_value = sample_event_list
    gamepad_recorder_with_mocked_methods.record_background()
    time.sleep(0.01)
    gamepad_recorder_with_mocked_methods.shutdown()

    with open(test_dir / "test.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        assert row[HN.TIMESTAMP] == str(sample_event_list[0].timestamp)
        assert row[HN.EVENT_TYPE] == sample_event_list[0].ev_type
        assert row[HN.PARAMETER_NAME] == sample_event_list[0].code
        assert row[HN.DATA_TYPE] == get_data_type_name(sample_event_list[0].state)
        assert row[HN.VALUE] == str(sample_event_list[0].state)

    Path(test_dir / "test.csv").unlink()
