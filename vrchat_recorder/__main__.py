"""Entry point for the vrchat_recorder package."""

import logging
import os
import sys
import time

import inputs

from . import confirm_preparation as confirm
from . import name_utils
from .argument_parser import get_parser
from .date_utils import get_now_str
from .gamepad_recorder import GamepadRecorder
from .obs_video_recorder import OBSVideoRecorder
from .osc_feedback_recorder import OSCFeedbackRecorder

root_logger = logging.getLogger()
stream_hdlr = logging.StreamHandler(sys.stdout)
root_logger.addHandler(stream_hdlr)

logger = logging.getLogger(__name__)


def main(arg_list=None):
    """Entry point for the vrchat_recorder package.

    Args:
        arg_list (list): List of arguments to parse. If None, sys.argv is used.
    """

    parser = get_parser()
    args = parser.parse_args(arg_list)

    output_dir = os.path.abspath(args.output_dir)
    date_format = args.date_format
    no_ask = args.no_ask
    log_level = args.log_level

    root_logger.setLevel(log_level)

    vrchat_osc_ip = args.vrchat_osc_ip
    vrchat_osc_port = args.vrchat_osc_port
    vrchat_osc_address = args.vrchat_osc_address
    vrchat_osc_server_timeout = args.vrchat_osc_server_timeout

    obs_websocket_ip = args.obs_websocket_ip
    obs_websocket_port = args.obs_websocket_port
    obs_websocket_password = args.obs_websocket_password

    no_osc_feedback = args.no_osc_feedback
    no_gamepad = args.no_gamepad
    no_obs = args.no_obs

    if not no_ask:
        confirm.confirm_about_vrchat(vrchat_osc_ip, vrchat_osc_port, vrchat_osc_address)
        confirm.confirm_about_obs(obs_websocket_ip, obs_websocket_port)

        if not no_gamepad:
            confirm.confirm_about_controller()

    vrcrec_dir_name = name_utils.get_vrcrec_dir_name(get_now_str(date_format))
    vrcrec_dir_path = os.path.join(output_dir, vrcrec_dir_name)

    os.makedirs(vrcrec_dir_path)

    background_recorders = []

    if not no_gamepad:
        if inputs.devices.gamepads == []:
            raise RuntimeError("No gamepad found.")

        gamepad_log_file_name = name_utils.get_gamepad_log_file_name(get_now_str(date_format))
        gamepad_log_file_path = os.path.join(vrcrec_dir_path, gamepad_log_file_name)
        gamepad_recorder = GamepadRecorder(gamepad_log_file_path)

        gamepad_recorder.record_background()
        logger.info(f"Start Gamepad Recording: {gamepad_log_file_path}")
        background_recorders.append(gamepad_recorder)

    if not no_osc_feedback:
        osc_feedback_log_file_name = name_utils.get_osc_feedback_log_file_name(get_now_str(date_format))
        osc_feedback_log_file_path = os.path.join(vrcrec_dir_path, osc_feedback_log_file_name)
        osc_feedback_recorder = OSCFeedbackRecorder(
            osc_feedback_log_file_path, vrchat_osc_ip, vrchat_osc_port, vrchat_osc_address, vrchat_osc_server_timeout
        )

        osc_feedback_recorder.record_background()
        logger.info(f"Start OSC Feedback Recording: {osc_feedback_log_file_path}")
        background_recorders.append(osc_feedback_recorder)

    if not no_obs:
        obs_video_file_name = name_utils.get_obs_video_file_name(get_now_str(date_format))
        obs_video_output_path = os.path.join(vrcrec_dir_path, obs_video_file_name)
        obs_video_recorder = OBSVideoRecorder(
            obs_video_output_path,
            obs_websocket_ip,
            obs_websocket_port,
            obs_websocket_password,
        )

        obs_video_recorder.record_background()
        logger.info(f"Start OBS Video Recording: {obs_video_output_path}")
        background_recorders.append(obs_video_recorder)

    logger.info("Press Ctrl+C to stop recording...")

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass

    for recorder in background_recorders:
        logger.info(f"Shutting down...: {recorder}")
        recorder.shutdown()

    logging.warning("If freezing, Press any controller button and play vrchat for a while.")


if __name__ == "__main__":
    main()
