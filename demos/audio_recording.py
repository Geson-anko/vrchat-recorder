import time
from pathlib import Path

import soundcard as sc

from vrchat_recorder.audio import MicRecorder, SpeakerRecorder

output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

mic_output_path = output_dir / "demo_mic_recording_%Y-%m-%d-%H-%M-%S-%f.wav"
speaker_output_path = output_dir / "demo_speaker_recording_%Y-%m-%d-%H-%M-%S-%f.wav"


mic_recorder = MicRecorder(
    str(mic_output_path), sc.default_microphone().name, sample_rate=44100, block_size=4096, num_channels=1
)
speaker_recorder = SpeakerRecorder(
    str(speaker_output_path), sc.default_speaker().name, sample_rate=44100, block_size=4096, num_channels=2
)


mic_recorder.record_background()
speaker_recorder.record_background()

print("Recording audios...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

mic_recorder.shutdown()
speaker_recorder.shutdown()

print("Done.")
