from pytest_mock import MockerFixture

from vrchat_recorder.audio import mic_recorder as mod
from vrchat_recorder.audio.mic_recorder import MicRecorder


def test_mic_recorder_init(mocker: MockerFixture):
    mock_sc = mocker.patch.object(mod, "sc")
    mock_sc.default_microphone.return_value = "default_mic"
    mock_sc.get_microphone.return_value = "mic"

    mr = MicRecorder(
        "path/to/output/<date format>.wav",
        "mic_name",
        sample_rate=48000,
        num_channels=2,
        block_size=4096,
        num_blocks_per_write=50,
        subtype="PCM_24",
    )

    assert mr.output_file_path_with_date_format == "path/to/output/<date format>.wav"
    assert mr.mic == "mic"
    assert mr.sample_rate == 48000
    assert mr.num_channels == 2
    assert mr.block_size == 4096
    assert mr.num_blocks_per_write == 50
    assert mr.subtype == "PCM_24"
