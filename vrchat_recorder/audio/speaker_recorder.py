from typing import Any, Optional

import soundcard as sc

from .audio_recorder import AudioRecorder


class SpeakerRecorder(AudioRecorder):
    """Records audio data from specified speaker to wav file."""

    def __init__(
        self, output_file_path_with_date_format: str, speaker_device_name: Optional[str] = None, **kwds: Any
    ) -> None:
        """Create a SpeakerRecorder object.

        If speaker_device_name is None, the default speaker will be used.
        Note: Speaker device is treated as a microphone device.
        So this class gets the speaker device as a microphone device using `get_microphone(name, include_loopback=True).

        Args:
            output_file_path_with_date_format (str): The path to the output file with date format.
            speaker_device_name (str): The name of the speaker device to record. You can know the name from `sc.all_speakers`.
            kwds (Any): The keyword arguments for AudioRecorder.
        """

        if speaker_device_name is None:
            speaker_device_name = sc.default_speaker().name

        speaker_device = sc.get_microphone(speaker_device_name, include_loopback=True)

        super().__init__(output_file_path_with_date_format, speaker_device, **kwds)
