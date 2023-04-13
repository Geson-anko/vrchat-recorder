import inputs
import pytest
from pytest_mock import MockerFixture

from vrchat_recorder import confirm_preparation as mod


@pytest.mark.parametrize(["OBS_WEBSOCKET_IP", "OBS_WEBSOCKET_PORT"], [("localhost", 4444), ("127.0.0.1", 9001)])
def test_confirm_about_obs(mocker: MockerFixture, OBS_WEBSOCKET_IP, OBS_WEBSOCKET_PORT):
    mock_input = mocker.patch("builtins.input", return_value="")
    mock_print = mocker.patch("builtins.print")

    mod.confirm_about_obs(OBS_WEBSOCKET_IP, OBS_WEBSOCKET_PORT)

    mock_print.assert_called_once_with(
        mod.confirm_about_obs_prompt.format(OBS_WEBSOCKET_IP, OBS_WEBSOCKET_PORT), end=""
    )
    mock_input.assert_called_once()


@pytest.mark.parametrize(
    ["VRCHAT_OSC_IP", "VRCHAT_OSC_PORT", "OSC_ADDRESS"],
    [("localhost", 9001, "/*"), ("127.0.0.7", 9000, "/avatar/parameters/*")],
)
def test_confirm_about_vrchat(mocker: MockerFixture, VRCHAT_OSC_IP, VRCHAT_OSC_PORT, OSC_ADDRESS):
    mock_input = mocker.patch("builtins.input", return_value="")
    mock_print = mocker.patch("builtins.print")

    mod.confirm_about_vrchat(VRCHAT_OSC_IP, VRCHAT_OSC_PORT, OSC_ADDRESS)

    mock_print.assert_called_once_with(
        mod.confirm_about_vrchat_prompt.format(VRCHAT_OSC_IP, VRCHAT_OSC_PORT, OSC_ADDRESS), end=""
    )

    mock_input.assert_called_once()


def test_confirm_about_controller(mocker: MockerFixture) -> None:
    # Mock the input and print functions
    mock_input = mocker.patch("builtins.input", return_value="")
    mock_print = mocker.patch("builtins.print")

    # Call the confirm_about_controller function
    mod.confirm_about_controller()

    # Check if the print function was called with the correct arguments
    expected_output = "\n".join([f"{i}: {controller.name}" for i, controller in enumerate(inputs.devices.gamepads)])
    mock_print.assert_called_once_with(mod.confirm_about_controller_prompt.format(expected_output), end="")

    # Check if the input function was called
    mock_input.assert_called_once()


def test_confirm_about_mic(mocker: MockerFixture) -> None:
    # Mock the input and print functions
    mock_input = mocker.patch("builtins.input", return_value="")
    mock_print = mocker.patch("builtins.print")
    mock_soundcard = mocker.patch("soundcard.all_microphones", return_value=[])

    # Call the confirm_about_mic function
    mod.confirm_about_mic("Microphone", 48000, 2)

    # Check if the print function was called with the correct arguments
    mock_print.assert_called_once_with(mod.confirm_about_mic_prompt.format("Microphone", 48000, 2, ""), end="")

    # Check if the input function was called
    mock_input.assert_called_once()

    # Check if the soundcard.all_microphones function was called
    mock_soundcard.assert_called_once()


def test_confirm_about_speaker(mocker: MockerFixture) -> None:
    # Mock the functions
    mock_input = mocker.patch("builtins.input", return_value="")
    mock_print = mocker.patch("builtins.print")
    mock_soundcard = mocker.patch("soundcard.all_microphones", return_value=[])

    # Call the confirm_about_speaker function
    mod.confirm_about_speaker("Speaker", 48000, 2)

    # Check if the print function was called with the correct arguments
    mock_print.assert_called_once_with(mod.confirm_about_speaker_prompt.format("Speaker", 48000, 2, ""), end="")

    # Check if the input function was called
    mock_input.assert_called_once()

    # Check if the soundcard.all_microphones function was called
    mock_soundcard.assert_called_once_with(include_loopback=True)


def test_confirm_about_vr_recoding(mocker: MockerFixture) -> None:
    # Mock the functions
    mock_input = mocker.patch("builtins.input", return_value="")
    mock_print = mocker.patch("builtins.print")

    # Call the confirm_about_vr_recording function
    mod.confirm_about_vr_recording(30.0)

    mock_print.assert_called_once_with(mod.confirm_about_vr_recording_prompt.format(30.0), end="")

    # Check if the input function was called
    mock_input.assert_called_once()
