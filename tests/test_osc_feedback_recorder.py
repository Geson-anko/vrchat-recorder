import csv
import tempfile
import time
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from vrchat_recorder.data_constants import CSVHeaderNames as HN
from vrchat_recorder.data_constants import get_data_type_name
from vrchat_recorder.osc_feedback_recorder import OSCFeedbackRecorder


def test_osc_feedback_recorder_init():
    output_file_path = Path(tempfile.TemporaryFile(suffix=".csv").name)
    host = "localhost"
    port = 9001
    address = "/avatar/parameters/*"

    ofr = OSCFeedbackRecorder(output_file_path, host, port, address)

    assert ofr.output_file_path == output_file_path
    assert ofr.host == host
    assert ofr.port == port
    assert ofr.address == address


@pytest.fixture
def osc_feedback_recorder_with_mocked_methods():
    output_file_path = Path(tempfile.TemporaryFile(suffix=".csv").name)
    host = "localhost"
    port = 9001
    address = "/avatar/parameters/*"

    ofr = OSCFeedbackRecorder(output_file_path, host, port, address)
    ofr._shutdown = False
    return ofr


@pytest.fixture
def pytest_mock_osc_server(mocker: MockerFixture):
    return mocker.patch("pythonosc.osc_server.ThreadingOSCUDPServer")


@pytest.fixture
def pytest_mock_dispatcher(mocker: MockerFixture):
    return mocker.patch("pythonosc.dispatcher.Dispatcher")


def test_osc_feedback_recorder_record(osc_feedback_recorder_with_mocked_methods, pytest_mock_osc_server):
    osc_feedback_recorder_with_mocked_methods.record_background()
    time.sleep(0.01)
    osc_feedback_recorder_with_mocked_methods.shutdown()

    assert pytest_mock_osc_server.called


def test_osc_feedback_recorder_osc_callback(osc_feedback_recorder_with_mocked_methods, mocker: MockerFixture):
    mocker.patch("time.time", return_value=0.0)

    output_file_path = osc_feedback_recorder_with_mocked_methods.output_file_path
    csv_headers = osc_feedback_recorder_with_mocked_methods.csv_headers
    with open(output_file_path, "a", newline="") as f:
        osc_feedback_recorder_with_mocked_methods.csv_writer = csv.DictWriter(f, fieldnames=csv_headers)
        address = "/avatar/parameters/Voice"
        value = 1.0
        osc_feedback_recorder_with_mocked_methods._osc_callback(address, value)

    with open(output_file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)

        assert float(row[HN.TIMESTAMP]) == 0.0
        assert row[HN.PARAMETER_NAME] == address
        assert row[HN.DATA_TYPE] == get_data_type_name(value)
        assert float(row[HN.VALUE]) == value

    output_file_path.unlink()
