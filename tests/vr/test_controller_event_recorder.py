import csv
import time
from pathlib import Path

import openvr
import pytest
from pytest_mock import MockerFixture

from vrchat_recorder.data_constants import CSVHeaderNames as HN
from vrchat_recorder.vr.controller_event_recorder import ControllerEventRecorder


def test_init(mocker: MockerFixture, tmp_path: Path):
    vrsystem_mock = mocker.MagicMock(spec=openvr.IVRSystem)
    output_file_path = tmp_path / "test_init.csv"
    poll_interval = 0.001
    flush_interval = 10.0

    recorder = ControllerEventRecorder(output_file_path, vrsystem_mock, poll_interval, flush_interval)

    assert recorder.output_file_path == output_file_path
    assert recorder.vrsystem == vrsystem_mock
    assert recorder.poll_interval == poll_interval
    assert recorder.flush_interval == flush_interval


def test_record(mocker: MockerFixture, tmp_path: Path, caplog: pytest.LogCaptureFixture):
    vrsystem_mock = mocker.MagicMock(spec=openvr.IVRSystem)
    output_file_path = tmp_path / "test_record.csv"
    poll_interval = 0.001

    recorder = ControllerEventRecorder(output_file_path, vrsystem_mock, poll_interval)
    recorder._record_controller_events = mocker.spy(recorder, "_record_controller_events")
    recorder.vrsystem.pollNextEvent.return_value = False
    recorder._flush_file_if_needed = mocker.spy(recorder, "_flush_file_if_needed")
    recorder._flush_file_if_needed.return_value = time.time()

    with caplog.at_level("DEBUG"):
        recorder.record_background()
        time.sleep(0.01)
        recorder.shutdown()

    recorder._record_controller_events.assert_called()
    recorder._flush_file_if_needed.assert_called()

    assert f"Recording controller events to {output_file_path}..." in caplog.messages
    assert "Recording finished." in caplog.messages


def test_is_controller_event(mocker: MockerFixture, tmp_path: Path):
    vrsystem_mock = mocker.Mock(spec=openvr.IVRSystem)
    event_mock = mocker.Mock()
    event_mock.trackedDeviceIndex = 0
    vrsystem_mock.getTrackedDeviceClass.return_value = openvr.TrackedDeviceClass_Controller

    recorder = ControllerEventRecorder(tmp_path / "test_is_controller_event.csv", vrsystem_mock)

    event_mock.eventType = openvr.VREvent_ButtonPress
    assert recorder._is_controller_event(event_mock)

    event_mock.eventType = openvr.VREvent_ButtonUnpress
    assert recorder._is_controller_event(event_mock)

    event_mock.eventType = openvr.VREvent_ButtonTouch
    assert recorder._is_controller_event(event_mock)

    event_mock.eventType = openvr.VREvent_ButtonUntouch
    assert recorder._is_controller_event(event_mock)

    event_mock.eventType = openvr.VREvent_TrackedDeviceUpdated
    assert not recorder._is_controller_event(event_mock)


def test_extract_event_data(mocker: MockerFixture, tmp_path: Path):
    vrsystem_mock = mocker.Mock()
    event_mock = mocker.Mock()
    event_mock.trackedDeviceIndex = 0
    event_mock.eventType = openvr.VREvent_ButtonPress
    event_mock.data.controller.button = 1
    event_mock.eventAgeSeconds = 0.01

    vrsystem_mock.getControllerRoleForTrackedDeviceIndex.return_value = openvr.TrackedControllerRole_RightHand

    recorder = ControllerEventRecorder(tmp_path / "tes_extract_event_data.csv", vrsystem_mock)
    timestamp = time.time()
    data = recorder._extract_event_data(event_mock, timestamp)

    assert data[HN.TIMESTAMP] == timestamp
    assert data[HN.EVENT_TYPE] == openvr.VREvent_ButtonPress
    assert data[HN.CONTROLLER_ROLE] == openvr.TrackedControllerRole_RightHand
    assert data[HN.BUTTON_ID] == 1
    assert data[HN.AGE_SECONDS] == 0.01


@pytest.fixture
def csvfile_mock(mocker: MockerFixture) -> MockerFixture:
    csvfile_mock = mocker.Mock()
    csvfile_mock.flush.return_value = None
    return csvfile_mock


def test_flush_file_if_needed(mocker: MockerFixture, csvfile_mock: MockerFixture, tmp_path: Path):
    vrsystem_mock = mocker.Mock()
    recorder = ControllerEventRecorder(tmp_path / "test_flush_file_if_needed.csv", vrsystem_mock)
    recorder.flush_interval = 1

    previous_flush = time.time() - 2
    recorder._flush_file_if_needed(csvfile_mock, previous_flush)
    csvfile_mock.flush.assert_called_once()

    previous_flush = time.time()
    csvfile_mock.flush.reset_mock()
    recorder._flush_file_if_needed(csvfile_mock, previous_flush)
    csvfile_mock.flush.assert_not_called()
