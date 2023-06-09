import json
import time
from unittest.mock import MagicMock

import numpy as np
import openvr
import pytest
from pytest_mock import MockerFixture

from vrchat_recorder.vr.binary_converter import holder_to_binary
from vrchat_recorder.vr.constants import HeaderNames, HeaderVersions
from vrchat_recorder.vr.tracking_data_holders import (
    Orientation,
    Position,
    create_empty_data_holder,
)
from vrchat_recorder.vr.tracking_recorder import (
    TrackingRecorder,
    binary_format,
    create_header,
)


@pytest.fixture
def tracking_recorder(mock_vrsystem):
    return TrackingRecorder("test_output.bin", mock_vrsystem, frame_rate=72)


def test_update_timestamp(mocker: MockerFixture, tracking_recorder):
    mocker.patch("time.time", return_value=1234567890.123456)
    tracking_recorder._update_timestamp()
    assert tracking_recorder._holder.timestamp == 1234567890.123456


def test_get_device_poses(tracking_recorder, mock_vrsystem):
    mock_device_poses = [MagicMock(spec=openvr.TrackedDevicePose_t) for _ in range(openvr.k_unMaxTrackedDeviceCount)]
    mock_vrsystem.getDeviceToAbsoluteTrackingPose.return_value = mock_device_poses

    device_poses = tracking_recorder._get_device_poses()
    assert len(device_poses) == openvr.k_unMaxTrackedDeviceCount
    mock_vrsystem.getDeviceToAbsoluteTrackingPose.assert_called_once()


def test_update_data_holder(tracking_recorder, mock_vrsystem):
    mock_device_poses = [MagicMock(spec=openvr.TrackedDevicePose_t) for _ in range(openvr.k_unMaxTrackedDeviceCount)]
    for device_pose in mock_device_poses:
        device_pose.bDeviceIsConnected = True
        device_pose.mDeviceToAbsoluteTracking = np.ones((3, 4), dtype=float)

    mock_vrsystem.getTrackedDeviceClass.return_value = openvr.TrackedDeviceClass_HMD
    mock_vrsystem.getControllerRoleForTrackedDeviceIndex.return_value = openvr.TrackedControllerRole_LeftHand

    holder = create_empty_data_holder()
    tracking_recorder._holder = holder
    tracking_recorder._update_data_holder(mock_device_poses)

    assert isinstance(tracking_recorder._holder.hmd.position, Position)
    assert isinstance(tracking_recorder._holder.hmd.orientation, Orientation)


def test_write_header(tracking_recorder: TrackingRecorder, tmp_path):
    test_file = tmp_path / "test_output_write_header.bin"
    tracking_recorder.output_file_path = str(test_file)

    header = create_header()
    with test_file.open("wb") as outfile:
        tracking_recorder._write_header(outfile)

    with test_file.open("rb") as outfile:
        header_size = int.from_bytes(outfile.read(4), "little")
        assert header_size == len(header)
        assert outfile.read(header_size) == header


def test_write_binary_data(tracking_recorder: TrackingRecorder, tmp_path):
    test_file = tmp_path / "test_output.bin"
    tracking_recorder.output_file_path = str(test_file)

    with test_file.open("wb") as outfile:
        frame_count = 0
        frame_count = tracking_recorder._write_binary_data(outfile, frame_count)

    assert frame_count == 1
    assert test_file.exists()
    assert test_file.stat().st_size == len(holder_to_binary(create_empty_data_holder()))


def test_record(caplog: pytest.LogCaptureFixture, tracking_recorder: TrackingRecorder, mocker: MockerFixture, tmp_path):
    test_file = tmp_path / "test_output.bin"
    tracking_recorder.output_file_path = str(test_file)

    tracking_recorder._write_header = mocker.spy(tracking_recorder, "_write_header")
    tracking_recorder._update_timestamp = mocker.spy(tracking_recorder, "_update_timestamp")
    tracking_recorder._get_device_poses = mocker.spy(tracking_recorder, "_get_device_poses")
    tracking_recorder._update_data_holder = mocker.spy(tracking_recorder, "_update_data_holder")
    tracking_recorder._write_binary_data = mocker.spy(tracking_recorder, "_write_binary_data")

    with caplog.at_level("DEBUG"):
        tracking_recorder.record_background()
        time.sleep(0.1)

        tracking_recorder.shutdown()  # to stop recording immediately

    tracking_recorder._write_header.assert_called_once()
    tracking_recorder._update_timestamp.assert_called()
    tracking_recorder._get_device_poses.assert_called()
    tracking_recorder._update_data_holder.assert_called()
    tracking_recorder._write_binary_data.assert_called()

    assert f"VR Tracking Recorder started. Output to {tracking_recorder.output_file_path}" in caplog.messages
    assert "VR Tracking Recorder stopped." in caplog.messages


def test_create_header():
    header = create_header()

    assert isinstance(header, bytes)

    header_dict = json.loads(header.decode("utf-8"))
    assert header_dict[HeaderNames.VERSION] == HeaderVersions.V0
    assert header_dict[HeaderNames.BINARY_FORMAT] == binary_format
