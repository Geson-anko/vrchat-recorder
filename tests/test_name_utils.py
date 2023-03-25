from unittest import mock

import pytest

from vrchat_recorder.data_constants import FileExtensions as FE
from vrchat_recorder.name_utils import (
    get_gamepad_log_file_name,
    get_obs_video_file_name,
    get_osc_feedback_log_file_name,
    get_vrcrec_dir_name,
)


@pytest.fixture
def date_str():
    return "2023-03-25"


def test_get_vrcrec_dir_name(date_str):
    expected_vrcrec_dir_name = f"{date_str}.{FE.VRCREC}"
    assert get_vrcrec_dir_name(date_str) == expected_vrcrec_dir_name


@mock.patch("inputs.devices.gamepads")
def test_get_gamepad_log_file_name(mock_gamepads, date_str):
    mock_gamepad = mock.MagicMock()
    mock_gamepad.name = "Test_Gamepad"
    mock_gamepads.__getitem__.return_value = mock_gamepad

    expected_gamepad_log_file_name = f"{date_str}.{mock_gamepad.name}.{FE.GAMEPAD}.{FE.CSV}"
    assert get_gamepad_log_file_name(date_str) == expected_gamepad_log_file_name


def test_get_osc_feedback_log_file_name(date_str):
    expected_osc_feedback_log_file_name = f"{date_str}.{FE.OSCFEEDBACK}.{FE.CSV}"
    assert get_osc_feedback_log_file_name(date_str) == expected_osc_feedback_log_file_name


def test_get_obs_video_file_name(date_str):
    expected_obs_video_file_name = f"{date_str}.{FE.VIDEO}"
    assert get_obs_video_file_name(date_str) == expected_obs_video_file_name
