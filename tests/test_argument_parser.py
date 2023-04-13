from argparse import ArgumentParser

from vrchat_recorder.argument_parser import (
    get_base_parser,
    get_mic_parser,
    get_obs_parser,
    get_osc_feedback_parser,
    get_speaker_parser,
    get_type_selection_parser,
)


def test_get_base_parser():
    parser = get_base_parser()

    assert parser.get_default("output_dir") == "./"
    assert parser.get_default("date_format") == "%Y-%m-%d-%H-%M-%S-%f"
    assert not parser.get_default("no_ask")
    assert parser.get_default("log_level") == "INFO"


def test_get_type_selection_parser():
    parser = ArgumentParser()
    parser = get_type_selection_parser(parser)

    assert not parser.get_default("no_osc_feedback")
    assert not parser.get_default("no_gamepad")
    assert not parser.get_default("no_obs")
    assert not parser.get_default("no_mic")
    assert not parser.get_default("no_speaker")


def test_get_osc_feedback_parser():
    parser = ArgumentParser()
    parser = get_osc_feedback_parser(parser)

    assert parser.get_default("vrchat_osc_ip") == "localhost"
    assert parser.get_default("vrchat_osc_port") == 9001
    assert parser.get_default("vrchat_osc_address") == "/avatar/parameters/*"
    assert parser.get_default("vrchat_osc_server_timeout") == 1.0


def test_get_obs_parser():
    parser = ArgumentParser()
    parser = get_obs_parser(parser)

    assert parser.get_default("obs_websocket_ip") == "localhost"
    assert parser.get_default("obs_websocket_port") == 4444
    assert parser.get_default("obs_websocket_password") == "password"


def test_get_mic_parser():
    parser = ArgumentParser()
    parser = get_mic_parser(parser)

    assert parser.get_default("mic_device_name") is None
    assert parser.get_default("mic_sample_rate") == 44100
    assert parser.get_default("mic_block_size") == 4096
    assert parser.get_default("mic_channels") == 1
    assert parser.get_default("mic_flush_interval") == 100
    assert parser.get_default("mic_subtype") == "PCM_16"


def test_get_speaker_parser():
    parser = ArgumentParser()
    parser = get_speaker_parser(parser)

    assert parser.get_default("speaker_device_name") is None
    assert parser.get_default("speaker_sample_rate") == 44100
    assert parser.get_default("speaker_block_size") == 4096
    assert parser.get_default("speaker_channels") == 2
    assert parser.get_default("speaker_flush_interval") == 100
    assert parser.get_default("speaker_subtype") == "PCM_16"
