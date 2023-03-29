"""This file contains the MicRecorder class."""


from typing import Any, Optional

import soundcard as sc

from .audio_recorder import AudioRecorder


class MicRecorder(AudioRecorder):
    """Records audio data from specified microphone to wav file."""

    def __init__(
        self, output_file_path_with_date_format: str, mic_device_name: Optional[str] = None, **kwds: Any
    ) -> None:
        """Create a MicRecorder object.

        If mic_device_name is None, the default microphone will be used.
        Args:
            output_file_path_with_date_format (str): The path to the output file with date format.
            mic_device_name (str): The name of the microphone device to record. You can know the name from `sc.all_microphones.
            kwds (Any): The keyword arguments for AudioRecorder.
        """

        if mic_device_name is None:
            mic_device = sc.default_microphone()
        else:
            mic_device = sc.get_microphone(mic_device_name)

        super().__init__(output_file_path_with_date_format, mic_device, **kwds)
