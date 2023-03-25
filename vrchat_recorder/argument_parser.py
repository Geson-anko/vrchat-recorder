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
