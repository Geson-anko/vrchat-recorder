import pytest
from pytest_mock import MockerFixture

from vrchat_recorder.vr.binary_converter import holder_to_binary
from vrchat_recorder.vr.tracking_data_holders import (
    VRDeviceTrackingDataHolder,
    create_empty_data_holder,
)
from vrchat_recorder.vr.tracking_reader import TrackingReader


@pytest.fixture
def test_file(tmp_path):
    test_file = tmp_path / "test_input.bin"
    holder = create_empty_data_holder()
    binary = holder_to_binary(holder)

    with test_file.open("wb") as f:
        f.write(binary)

    return test_file


@pytest.fixture
def tracking_reader(test_file):
    return TrackingReader(str(test_file))


def test_init(tracking_reader: TrackingReader, test_file):
    assert tracking_reader.input_file_path == str(test_file)
    assert tracking_reader.num_frames == 1
    assert tracking_reader.read_count == 0


def test_reset(tracking_reader: TrackingReader):
    tracking_reader._file.seek(10)
    tracking_reader.reset()
    assert tracking_reader._file.tell() == 0


def test_read(tracking_reader: TrackingReader):
    data_holder = tracking_reader.read()
    assert isinstance(data_holder, VRDeviceTrackingDataHolder)
    assert tracking_reader.read_count == 1


def test_read_eof(tracking_reader: TrackingReader):
    tracking_reader.read()
    assert tracking_reader.read() is None


def test_close(tracking_reader: TrackingReader):
    tracking_reader.close()
    assert tracking_reader._file.closed


def test_repr(tracking_reader: TrackingReader, test_file):
    assert repr(tracking_reader) == f"TrackingReader(input_file_path={str(test_file)},)"


def test_del(tracking_reader: TrackingReader, mocker: MockerFixture):
    mock_close = mocker.patch.object(TrackingReader, "close")
    tracking_reader.__del__()
    mock_close.assert_called_once()
