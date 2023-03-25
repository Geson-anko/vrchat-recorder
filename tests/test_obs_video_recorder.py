import shutil
from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from vrchat_recorder.obs_video_recorder import OBSVideoRecorder


class MockOBSClient:
    def __init__(self, host, port, password):
        self.output_path = "test_output.mkv"

    def start_record(self):
        pass

    def stop_record(self):
        return MagicMock(output_path=self.output_path)


def test_OBSVideoRecorder(mocker: MockerFixture):
    mocker.patch("obsws_python.ReqClient", new=MockOBSClient)

    # Test initializing OBSVideoRecorder
    output_file_path = "test_output"
    host = "localhost"
    port = 4444
    password = "password"
    recorder = OBSVideoRecorder(output_file_path, host, port, password)

    # Test record method
    mocker.patch("time.sleep", lambda x: recorder.shutdown())
    mocker.patch("shutil.move", autospec=True)

    recorder.record()

    shutil.move.assert_called_once()
    args, kwargs = shutil.move.call_args
    assert args[0] == "test_output.mkv"
    assert args[1].startswith("test_output.")
    assert args[1].endswith(".mkv")
