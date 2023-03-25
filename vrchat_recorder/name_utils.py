"""This file contains tools for generating file or directory names. We can generate following names.

- `.vrcrec` directory: `<date>.vrcrec`
- gamepad log file: `<date>.<gamepad name>.gamepad.csv`
- osc feedback log file: `<date>.oscfb.csv`
- OBS video (and audio) file: `<date>.video.<ext>`
"""

from inputs import devices

from .data_constants import FileExtensions as FE


def get_vrcrec_dir_name(date_str: str) -> str:
    """Get the name of the `.vrcrec` directory.
    Args:
        date_str: (str): The date string.

    Returns:
        vrc rec directory name. (str): The name of the `.vrcrec` directory.
    """

    return f"{date_str}.{FE.VRCREC}"


def get_gamepad_log_file_name(date_str: str) -> str:
    """Get the name of the gamepad log file.
    Args:
        date_str: (str): The date string.

    Returns:
        gamepad log file name. (str): The name of the gamepad log file.
    """
    return f"{date_str}.{devices.gamepads[0].name}.{FE.GAMEPAD}.{FE.CSV}"


def get_osc_feedback_log_file_name(date_str: str) -> str:
    """Get the name of the OSC feedback log file.
    Args:
        date_str: (str): The date string.

    Returns:
        osc feedback log file name. (str): The name of the OSC feedback log file.
    """
    return f"{date_str}.{FE.OSCFEEDBACK}.{FE.CSV}"


def get_obs_video_file_name(date_str: str) -> str:
    """Get the name of the OBS video file.
    Args:
        date_str: (str): The date string.

    Returns:
        obs video file name. (str): The name of the OBS video file.
    """
    return f"{date_str}.{FE.VIDEO}"
