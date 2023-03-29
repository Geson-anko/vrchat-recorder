"""This file contains the AudioRecorder class."""
import logging
import sys

import soundfile as sf

if sys.platform == "win32":
    from soundcard.mediafoundation import _Microphone
elif sys.platform == "linux":
    from soundcard.pulseaudio import _Microphone
elif sys.platform == "darwin":
    from soundcard.coreaudio import _Microphone

from ..abc.base_recorder import BaseRecorder
from ..date_utils import get_now_str

logger = logging.getLogger(__name__)


class AudioRecorder(BaseRecorder):
    """Records audio data from the specified device to wav file.

    Usage:
        ```python
        from vrchat_recorder.audio.audio_recorder import AudioRecorder

        ar = AudioRecorder("path/to/output/<date format>.wav", "<device>")
        ar.record_background()
        ```
    The <date format> is the same as the `strftime` format. File name will be determined when the recording starts.
    """

    def __init__(
        self,
        output_file_path_with_date_format: str,
        mic_device: _Microphone,
        sample_rate: int = 44100,
        num_channels: int = 1,
        block_size: int = 2048,
        num_blocks_per_write: int = 100,
        subtype="PCM_16",
    ) -> None:
        """Create a AudioRecorder object.

        Args:
            output_file_path_with_date_format (str): The path to the output file with date format.
            device (str): The device to record. You can get the device by `sc.get_microphone`.
            sample_rate (int): The sample rate of the recording.
            num_channels (int): The number of channels of the recording.
            block_size (int): The block size of the recording.
            num_blocks_per_write (int): The number of blocks to flush to the file at once.
            subtype (str): The subtype of the recording.
        """

        self.output_file_path_with_date_format = output_file_path_with_date_format
        self.mic = mic_device
        self.sample_rate = sample_rate
        self.num_channels = num_channels
        self.block_size = block_size
        self.num_blocks_per_write = num_blocks_per_write
        self.subtype = subtype

    def record(self):
        """Record data to the output file until Keyboard interrupt or shutdown.

        You can quit the recording by pressing Ctrl+C or `self.shutdown()` (setting `self._shutdown` to True).
        """
        output_file_path = get_now_str(self.output_file_path_with_date_format)
        logger.info(f"Recording audio to {output_file_path} ...")

        frames_written = 0
        with sf.SoundFile(
            output_file_path, "x", samplerate=self.sample_rate, channels=self.num_channels, subtype=self.subtype
        ) as f:
            with self.mic.recorder(
                samplerate=self.sample_rate, blocksize=self.block_size, channels=self.num_channels
            ) as mic:
                try:
                    while not self._shutdown:
                        data = mic.record(numframes=self.block_size)
                        f.write(data)
                        frames_written += self.block_size
                        if frames_written % (self.block_size * self.num_blocks_per_write) == 0:
                            f.flush()
                except KeyboardInterrupt:
                    pass

        logger.info(f"Audio recording finished. {frames_written} frames written to {output_file_path}.")
