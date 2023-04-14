"""This file contains the tool for parsing command line arguments."""
from argparse import ArgumentParser


def get_parser() -> ArgumentParser:
    """Create a parser for the recorder.

    Returns:
        parser (ArgumentParser): The parser.
    """

    parser = get_base_parser()
    parser = get_type_selection_parser(parser)
    parser = get_osc_feedback_parser(parser)
    parser = get_obs_parser(parser)
    parser = get_mic_parser(parser)
    parser = get_speaker_parser(parser)
    parser = get_vr_parser(parser)

    return parser


def get_base_parser() -> ArgumentParser:
    """Create a base paraser for the recorder.

    Returns:
        parser (ArgumentParser): The base parser.
    """

    parser = ArgumentParser()
    parser.add_argument("-d", "--output_dir", default="./", help="The directory to save the output files.")
    parser.add_argument("--date_format", default="%Y-%m-%d-%H-%M-%S-%f", help="The format of the date string.")
    parser.add_argument("--no_ask", action="store_true", help="Do not ask for confirmation before recording.")
    parser.add_argument(
        "--log_level", default="INFO", help="The log level.", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    )
    return parser


def get_type_selection_parser(parser: ArgumentParser) -> ArgumentParser:
    """Create a parser for selecting the record type.

    Args:
        parser (ArgumentParser): The base parser.

    Returns:
        parser (ArgumentParser): The record type selector parser.
    """

    parser.add_argument("--no_osc_feedback", action="store_true", help="Do not record the OSC feedback.")
    parser.add_argument("--no_gamepad", action="store_true", help="Do not record the gamepad input.")
    parser.add_argument("--no_obs", action="store_true", help="Do not control OBS and play video is not recorded.")
    parser.add_argument("--no_mic", action="store_true", help="Do not record the microphone.")
    parser.add_argument("--no_speaker", action="store_true", help="Do not record the speaker.")
    parser.add_argument("--no_vr", action="store_true", help="Do not record the VR tracking data.")

    return parser


def get_osc_feedback_parser(parser: ArgumentParser) -> ArgumentParser:
    """Create a parser for the OSC feedback recorder.

    Args:
        parser (ArgumentParser): The base parser.

    Returns:
        parser (ArgumentParser): The OSC feedback parser.
    """

    parser.add_argument("--vrchat_osc_ip", default="localhost", help="The IP address of the VRChat OSC server.")
    parser.add_argument("--vrchat_osc_port", type=int, default=9001, help="The port of the VRChat OSC server.")
    parser.add_argument("--vrchat_osc_address", default="/avatar/parameters/*", help="The OSC address to record.")
    parser.add_argument("--vrchat_osc_server_timeout", type=float, default=1.0, help="The timeout for the OSC server.")

    return parser


def get_obs_parser(parser: ArgumentParser) -> ArgumentParser:
    """Create a parser for the OBS controlling.

    Args:
        parser (ArgumentParser): The base parser.

    Returns:
        parser (ArgumentParser): The argument parser for controlling obs.
    """
    parser.add_argument("--obs_websocket_ip", default="localhost", help="The IP address of the OBS websocket server.")
    parser.add_argument("--obs_websocket_port", type=int, default=4444, help="The port of the OBS websocket server.")
    parser.add_argument(
        "--obs_websocket_password", default="password", help="The password of the OBS websocket server."
    )

    return parser


def get_mic_parser(parser: ArgumentParser) -> ArgumentParser:
    """Create a parser for the microphone recording.

    Args:
        parser (ArgumentParser): The base parser.

    Returns:
        parser (ArgumentParser): The argument parser for recording the microphone.
    """

    parser.add_argument("--mic_device_name", "--mic", default=None, help="The name of the microphone device.")
    parser.add_argument("--mic_sample_rate", type=int, default=44100, help="The sample rate of the microphone.")
    parser.add_argument("--mic_block_size", type=int, default=4096, help="The chunk size of the microphone.")
    parser.add_argument("--mic_channels", type=int, default=1, help="The number of channels of the microphone.")
    parser.add_argument(
        "--mic_flush_interval", type=int, default=100, help="The number of blocks to flush to the file at once."
    )
    parser.add_argument("--mic_subtype", default="PCM_16", help="The subtype of the microphone recording data.")

    return parser


def get_speaker_parser(parser: ArgumentParser) -> ArgumentParser:
    """Create a parser for the speaker recording.

    Args:
        parser (ArgumentParser): The base parser.

    Returns:
        parser (ArgumentParser): The argument parser for recording the speaker.
    """

    parser.add_argument("--speaker_device_name", "--speaker", default=None, help="The name of the speaker device.")
    parser.add_argument("--speaker_sample_rate", type=int, default=44100, help="The sample rate of the speaker.")
    parser.add_argument("--speaker_block_size", type=int, default=4096, help="The chunk size of the speaker.")
    parser.add_argument("--speaker_channels", type=int, default=2, help="The number of channels of the speaker.")
    parser.add_argument(
        "--speaker_flush_interval", type=int, default=100, help="The number of blocks to flush to the file at once."
    )
    parser.add_argument("--speaker_subtype", default="PCM_16", help="The subtype of the speaker recording data.")

    return parser


def get_vr_parser(parser: ArgumentParser) -> ArgumentParser:
    """Create a parser for recording VR information.

    Args:
        parser (ArgumentParser): The base parser.

    Returns:
        parser (ArgumentParser): The argument parser for recording the VR.
    """

    parser.add_argument("--vr_tracking_fps", type=float, default=72.0, help="The FPS of the VR tracking data.")
    parser.add_argument(
        "--vr_tracking_flush_interval",
        type=int,
        default=1000,
        help="The number of frames to flush to the file at once.",
    )
    parser.add_argument(
        "--vr_controller_event_poll_interval",
        type=float,
        default=0.001,
        help="The interval to poll the controller events.",
    )
    parser.add_argument(
        "--vr_controller_event_flush_interval_seconds",
        type=float,
        default=10.0,
        help="The interval to flush the controller events.",
    )

    return parser
