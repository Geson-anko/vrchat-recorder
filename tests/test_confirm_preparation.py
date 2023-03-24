from io import StringIO
from unittest.mock import patch

import pytest

from vrchat_recorder import confirm_preparation as mod


@pytest.mark.parametrize(["OBS_WEBSOCKET_IP", "OBS_WEBSOCKET_PORT"], [("localhost", 4444), ("127.0.0.1", 9001)])
def test_confirm_about_obs(OBS_WEBSOCKET_IP, OBS_WEBSOCKET_PORT):
    with patch("builtins.input", return_value=""):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            mod.confirm_about_obs(OBS_WEBSOCKET_IP, OBS_WEBSOCKET_PORT)

    assert fake_out.getvalue() == mod.confirm_about_obs_prompt.format(OBS_WEBSOCKET_IP, OBS_WEBSOCKET_PORT)


@pytest.mark.parametrize(
    ["VRCHAT_OSC_IP", "VRCHAT_OSC_PORT", "OSC_ADDRESS"],
    [("localhost", 9001, "/*"), ("127.0.0.7", 9000, "/avatar/parameters/*")],
)
def test_confirm_about_vrchat(VRCHAT_OSC_IP, VRCHAT_OSC_PORT, OSC_ADDRESS):
    with patch("builtins.input", return_value=""):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            mod.confirm_about_vrchat(VRCHAT_OSC_IP, VRCHAT_OSC_PORT, OSC_ADDRESS)

    assert fake_out.getvalue() == mod.confirm_about_vrchat_prompt.format(VRCHAT_OSC_IP, VRCHAT_OSC_PORT, OSC_ADDRESS)
