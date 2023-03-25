import tempfile
from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from vrchat_recorder import confirm_preparation as confirm
from vrchat_recorder.__main__ import main
from vrchat_recorder.gamepad_recorder import GamepadRecorder
from vrchat_recorder.obs_video_recorder import OBSVideoRecorder
from vrchat_recorder.osc_feedback_recorder import OSCFeedbackRecorder


def test_main(mocker: MockerFixture):
    test_dir = tempfile.TemporaryDirectory().name

    # Mock confirm_preparation
    mocker.patch.object(confirm, "confirm_about_vrchat", MagicMock())
    mocker.patch.object(confirm, "confirm_about_obs", MagicMock())
    mocker.patch.object(confirm, "confirm_about_controller", MagicMock())

    # Mock GamepadRecorder
    mocker.patch.object(GamepadRecorder, "__init__", MagicMock(return_value=None))
    mocker.patch.object(GamepadRecorder, "record_background", MagicMock())
    mocker.patch.object(GamepadRecorder, "shutdown", MagicMock())

    # Mock Gamepad
    gamepad = MagicMock()
    gamepad.name = "Gamepad"
    mocker.patch("inputs.devices.gamepads", MagicMock(return_value=[gamepad]))

    # Mock OSCFeedbackRecorder
    mocker.patch.object(OSCFeedbackRecorder, "__init__", MagicMock(return_value=None))
    mocker.patch.object(OSCFeedbackRecorder, "record_background", MagicMock())
    mocker.patch.object(OSCFeedbackRecorder, "shutdown", MagicMock())

    # Mock OBSVideoRecorder
    mocker.patch.object(OBSVideoRecorder, "__init__", MagicMock(return_value=None))
    mocker.patch.object(OBSVideoRecorder, "record_background", MagicMock())
    mocker.patch.object(OBSVideoRecorder, "shutdown", MagicMock())

    # Mock time.sleep to raise KeyboardInterrupt after the first call
    mocker.patch("time.sleep", MagicMock(side_effect=KeyboardInterrupt))

    main(["--output_dir", test_dir])  # Pass empty list to use default values

    # Assert that confirm_preparation functions are called
    confirm.confirm_about_vrchat.assert_called_once()
    confirm.confirm_about_obs.assert_called_once()
    confirm.confirm_about_controller.assert_called_once()

    # Assert that the recorders are initialized and their methods are called
    GamepadRecorder.__init__.assert_called_once()
    GamepadRecorder.record_background.assert_called_once()
    GamepadRecorder.shutdown.assert_called_once()

    OSCFeedbackRecorder.__init__.assert_called_once()
    OSCFeedbackRecorder.record_background.assert_called_once()
    OSCFeedbackRecorder.shutdown.assert_called_once()

    OBSVideoRecorder.__init__.assert_called_once()
    OBSVideoRecorder.record_background.assert_called_once()
    OBSVideoRecorder.shutdown.assert_called_once()
