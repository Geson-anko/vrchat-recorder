from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from vrchat_recorder.audio import audio_recorder as mod
from vrchat_recorder.audio.audio_recorder import AudioRecorder, _Microphone

output_file_path = "path/to/output/2021-01-01-00-00-00.wav"


@pytest.fixture
def mock_mic_device():
    return MagicMock(spec=_Microphone)


@pytest.fixture
def audio_recorder(mock_mic_device):
    return AudioRecorder(output_file_path, mock_mic_device)


def test_audio_recorder_init(mock_mic_device):
    ar = AudioRecorder(
        "path/to/output/<date format>.wav",
        mock_mic_device,
        sample_rate=48000,
        num_channels=2,
        block_size=4096,
        num_blocks_per_write=50,
    )

    assert ar.output_file_path_with_date_format == "path/to/output/<date format>.wav"
    assert ar.mic == mock_mic_device
    assert ar.sample_rate == 48000
    assert ar.num_channels == 2
    assert ar.block_size == 4096
    assert ar.num_blocks_per_write == 50
    assert ar.subtype == "PCM_16"


def test_audio_recorder_record(caplog: pytest.LogCaptureFixture, mocker: MockerFixture, audio_recorder: AudioRecorder):

    mock_get_now_str = mocker.patch.object(mod, "get_now_str", return_value=output_file_path)
    mock_sf = mocker.patch("soundfile.SoundFile")
    mock_recorder = mocker.patch.object(audio_recorder.mic, "recorder", return_value=MagicMock())

    # Set the loop to run twice before the shutdown
    audio_recorder._shutdown = False
    audio_recorder.block_size = 2048
    loop_count = 2

    def stop_after_loops(*args, **kwargs):
        nonlocal loop_count
        if loop_count <= 0:
            audio_recorder._shutdown = True
        else:
            loop_count -= 1

    mock_recorder.return_value.__enter__.return_value.record.side_effect = stop_after_loops
    with caplog.at_level("DEBUG"):
        audio_recorder.record()

    assert f"Recording audio to {output_file_path} ..." in caplog.messages
    assert (
        f"Audio recording finished. {audio_recorder.block_size * 3} frames written to {output_file_path}."
        in caplog.text
    )

    assert mock_recorder.return_value.__enter__.return_value.record.call_count == 3
    mock_sf.assert_called_once_with(
        output_file_path,
        "x",
        samplerate=audio_recorder.sample_rate,
        channels=audio_recorder.num_channels,
        subtype=audio_recorder.subtype,
    )
    mock_recorder.assert_called_once_with(
        samplerate=audio_recorder.sample_rate, blocksize=audio_recorder.block_size, channels=audio_recorder.num_channels
    )
    mock_get_now_str.assert_called_once_with(audio_recorder.output_file_path_with_date_format)
