"""Entry point for the vrchat_recorder package."""

import logging
import os
import sys
import time

import inputs
import openvr
import soundcard as sc

from . import confirm_preparation as confirm
from . import name_utils
from .argument_parser import get_parser
from .audio import MicRecorder, SpeakerRecorder
from .date_utils import get_now_str
from .gamepad_recorder import GamepadRecorder
from .obs_video_recorder import OBSVideoRecorder
from .osc_feedback_recorder import OSCFeedbackRecorder
from .vr import ControllerEventRecorder, TrackingRecorder

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

    mic_device_name = args.mic_device_name if args.mic_device_name is not None else sc.default_microphone().name
    mic_sample_rate = args.mic_sample_rate
    mic_block_size = args.mic_block_size
    mic_channels = args.mic_channels
    mic_flush_interval = args.mic_flush_interval
    mic_subtype = args.mic_subtype

    speaker_device_name = (
        args.speaker_device_name if args.speaker_device_name is not None else sc.default_speaker().name
    )
    speaker_sample_rate = args.speaker_sample_rate
    speaker_block_size = args.speaker_block_size
    speaker_channels = args.speaker_channels
    speaker_flush_interval = args.speaker_flush_interval
    speaker_subtype = args.speaker_subtype

    vr_tracking_fps = args.vr_tracking_fps
    vr_tracking_flush_interval = args.vr_tracking_flush_interval
    vr_controller_event_poll_interval = args.vr_controller_event_poll_interval
    vr_controller_event_flush_interval_seconds = args.vr_controller_event_flush_interval_seconds

    no_osc_feedback = args.no_osc_feedback
    no_gamepad = args.no_gamepad
    no_obs = args.no_obs
    no_mic = args.no_mic
    no_speaker = args.no_speaker
    no_vr = args.no_vr

    if not no_ask:
        confirm.confirm_about_vrchat(vrchat_osc_ip, vrchat_osc_port, vrchat_osc_address)
        confirm.confirm_about_obs(obs_websocket_ip, obs_websocket_port)

        if not no_gamepad:
            confirm.confirm_about_gamepad()

        if not no_mic:
            confirm.confirm_about_mic(mic_device_name, mic_sample_rate, mic_channels)

        if not no_speaker:
            confirm.confirm_about_speaker(speaker_device_name, speaker_sample_rate, speaker_channels)

        if not no_vr:
            confirm.confirm_about_vr_recording(vr_tracking_fps)

    else:
        logger.info("Skipping confirmation.")

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

    audio_dir_path = os.path.join(vrcrec_dir_path, "audio")
    os.makedirs(audio_dir_path, exist_ok=True)

    if not no_mic:
        mic_file_name_with_datefmt = name_utils.get_mic_audio_file_name(
            date_format
        )  # Date is determined when the recording starts.
        mic_output_path = os.path.join(audio_dir_path, mic_file_name_with_datefmt)
        mic_recorder = MicRecorder(
            mic_output_path,
            mic_device_name,
            sample_rate=mic_sample_rate,
            num_channels=mic_channels,
            block_size=mic_block_size,
            num_blocks_per_write=mic_flush_interval,
            subtype=mic_subtype,
        )

        mic_recorder.record_background()
        logger.info(f"Start Mic Recording: {mic_output_path}")
        background_recorders.append(mic_recorder)

    if not no_speaker:
        speaker_file_name_with_datefmt = name_utils.get_speaker_audio_file_name(date_format)
        speaker_output_path = os.path.join(audio_dir_path, speaker_file_name_with_datefmt)
        speaker_recorder = SpeakerRecorder(
            speaker_output_path,
            speaker_device_name,
            sample_rate=speaker_sample_rate,
            num_channels=speaker_channels,
            block_size=speaker_block_size,
            num_blocks_per_write=speaker_flush_interval,
            subtype=speaker_subtype,
        )

        speaker_recorder.record_background()
        logger.info(f"Start Speaker Recording: {speaker_output_path}")
        background_recorders.append(speaker_recorder)

    if not no_vr:
        vr_dir_path = os.path.join(vrcrec_dir_path, "vr")
        os.makedirs(vr_dir_path, exist_ok=True)
        vrsystem = openvr.init(openvr.VRApplication_Background)

        vr_tracking_file_name = name_utils.get_vr_tracking_log_file_name(get_now_str(date_format))
        vr_tracking_output_path = os.path.join(vr_dir_path, vr_tracking_file_name)
        vr_tracking_recorder = TrackingRecorder(
            vr_tracking_output_path,
            vrsystem,
            vr_tracking_fps,
            vr_tracking_flush_interval,
        )

        vr_controller_event_file_name = name_utils.get_vr_controller_event_log_file_name(get_now_str(date_format))
        vr_controller_event_output_path = os.path.join(vr_dir_path, vr_controller_event_file_name)
        vr_controller_event_recorder = ControllerEventRecorder(
            vr_controller_event_output_path,
            vrsystem,
            vr_controller_event_poll_interval,
            vr_controller_event_flush_interval_seconds,
        )

        logger.info(f"Start VR Device Recording: {vr_dir_path}")
        vr_tracking_recorder.record_background()
        vr_controller_event_recorder.record_background()
        background_recorders.append(vr_tracking_recorder)
        background_recorders.append(vr_controller_event_recorder)

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
