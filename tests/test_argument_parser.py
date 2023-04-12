from argparse import ArgumentParser

import pytest

from vrchat_recorder.argument_parser import get_parser


@pytest.fixture
def parser() -> ArgumentParser:
    return get_parser()


def test_default_values(parser: ArgumentParser):
    args = parser.parse_args([])

    assert args.output_dir == "./"
    assert args.date_format == "%Y-%m-%d-%H-%M-%S-%f"
    assert not args.no_ask
    assert args.log_level == "INFO"

    assert not args.no_osc_feedback
    assert not args.no_gamepad
    assert not args.no_obs
    assert not args.no_mic
    assert not args.no_speaker

    assert args.vrchat_osc_ip == "localhost"
    assert args.vrchat_osc_port == 9001
    assert args.vrchat_osc_address == "/avatar/parameters/*"
    assert args.vrchat_osc_server_timeout == 1.0

    assert args.obs_websocket_ip == "localhost"
    assert args.obs_websocket_port == 4444
    assert args.obs_websocket_password == "password"

    assert args.mic_device_name is None
    assert args.mic_sample_rate == 44100
    assert args.mic_block_size == 4096
    assert args.mic_channels == 1
    assert args.mic_flush_interval == 100
    assert args.mic_subtype == "PCM_16"

    assert args.speaker_device_name is None
    assert args.speaker_sample_rate == 44100
    assert args.speaker_block_size == 4096
    assert args.speaker_channels == 2
    assert args.speaker_flush_interval == 100
    assert args.speaker_subtype == "PCM_16"


def test_custom_values(parser: ArgumentParser):
    custom_args = [
        "--output_dir",
        "/custom/output/dir",
        "--date_format",
        "%Y-%m-%d",
        "--no_ask",
        "--log_level",
        "DEBUG",
        "--no_osc_feedback",
        "--no_gamepad",
        "--no_obs",
        "--no_mic",
        "--no_speaker",
        "--vrchat_osc_ip",
        "192.168.1.1",
        "--vrchat_osc_port",
        "8000",
        "--vrchat_osc_address",
        "/custom/osc/address/*",
        "--vrchat_osc_server_timeout",
        "2.0",
        "--obs_websocket_ip",
        "10.0.0.1",
        "--obs_websocket_port",
        "5000",
        "--obs_websocket_password",
        "custom_password",
        "--mic_device_name",
        "custom_mic_device_name",
        "--mic_sample_rate",
        "48000",
        "--mic_block_size",
        "2048",
        "--mic_channels",
        "2",
        "--mic_flush_interval",
        "200",
        "--mic_subtype",
        "PCM_24",
        "--speaker_device_name",
        "custom_speaker_device_name",
        "--speaker_sample_rate",
        "48000",
        "--speaker_block_size",
        "2048",
        "--speaker_channels",
        "2",
        "--speaker_flush_interval",
        "200",
        "--speaker_subtype",
        "PCM_24",
    ]

    args = parser.parse_args(custom_args)

    assert args.output_dir == "/custom/output/dir"
    assert args.date_format == "%Y-%m-%d"
    assert args.no_ask
    assert args.log_level == "DEBUG"

    assert args.no_osc_feedback
    assert args.no_gamepad
    assert args.no_obs
    assert args.no_mic
    assert args.no_speaker

    assert args.vrchat_osc_ip == "192.168.1.1"
    assert args.vrchat_osc_port == 8000
    assert args.vrchat_osc_address == "/custom/osc/address/*"
    assert args.vrchat_osc_server_timeout == 2.0

    assert args.obs_websocket_ip == "10.0.0.1"
    assert args.obs_websocket_port == 5000
    assert args.obs_websocket_password == "custom_password"

    assert args.mic_device_name == "custom_mic_device_name"
    assert args.mic_sample_rate == 48000
    assert args.mic_block_size == 2048
    assert args.mic_channels == 2
    assert args.mic_flush_interval == 200
    assert args.mic_subtype == "PCM_24"

    assert args.speaker_device_name == "custom_speaker_device_name"
    assert args.speaker_sample_rate == 48000
    assert args.speaker_block_size == 2048
    assert args.speaker_channels == 2
    assert args.speaker_flush_interval == 200
    assert args.speaker_subtype == "PCM_24"
