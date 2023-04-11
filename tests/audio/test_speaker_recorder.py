from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from vrchat_recorder.audio import speaker_recorder as mod
from vrchat_recorder.audio.speaker_recorder import SpeakerRecorder


def test_speaker_recorder_init(mocker: MockerFixture):
    mock_sc = mocker.patch.object(mod, "sc")
    mock_sc.default_speaker.return_value = MagicMock(name="default_speaker")
    mock_sc.default_speaker.return_value.name = "default_speaker_name"
    mock_sc.get_microphone.return_value = "speaker"

    sr = SpeakerRecorder(
        "path/to/output/<date format>.wav",
        "speaker_name",
        sample_rate=48000,
        num_channels=2,
        block_size=4096,
        num_blocks_per_write=50,
        subtype="PCM_16",
    )

    assert sr.output_file_path_with_date_format == "path/to/output/<date format>.wav"
    assert sr.mic == "speaker"
    assert sr.sample_rate == 48000
    assert sr.num_channels == 2
    assert sr.block_size == 4096
    assert sr.num_blocks_per_write == 50
    assert sr.subtype == "PCM_16"
