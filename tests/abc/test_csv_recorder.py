import csv
import tempfile
import threading
from pathlib import Path

import pytest

from vrchat_recorder.abc.csv_recorder import CSVRecorder


class TestCSVRecorderImpl(CSVRecorder):
    def record(self):
        with open(self.output_file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["test", "data"])


def test_CSVRecorder(caplog: pytest.LogCaptureFixture):
    caplog.set_level(0)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)

        # Test creating a new file with headers
        output_file = tmp_dir / "test_output.csv"
        headers = ["Column1", "Column2"]
        recorder = TestCSVRecorderImpl(output_file, csv_headers=headers)
        assert recorder.output_file_path == output_file
        assert recorder._shutdown is False
        assert recorder.csv_headers == headers

        assert output_file.exists()

        with open(output_file) as f:
            reader = csv.reader(f)
            assert list(reader) == [headers]

        # Test existing file with matching headers
        recorder = TestCSVRecorderImpl(output_file, csv_headers=headers)

        # Test logger warning when file exists
        assert f"Output file already exists: {output_file}" in caplog.text

        # Test existing file with mismatched headers
        with pytest.raises(ValueError):
            recorder = TestCSVRecorderImpl(output_file, csv_headers=["Different", "Headers"])

        # Test record method
        recorder.record()
        assert recorder.backgroud_thread is None
        with open(output_file) as f:
            reader = csv.reader(f)
            assert list(reader) == [headers, ["test", "data"]]

        # Test background recording
        recorder.record_background()
        assert isinstance(recorder.backgroud_thread, threading.Thread)

        # Test logger info when background recording starts
        assert "Started background recording." in caplog.text

        recorder.shutdown()
        assert recorder._shutdown is True

        # Test logger info when background recording is shut down
        assert "Shutdown background recording." in caplog.text

        with open(output_file) as f:
            reader = csv.reader(f)
            assert list(reader) == [headers, ["test", "data"], ["test", "data"]]
