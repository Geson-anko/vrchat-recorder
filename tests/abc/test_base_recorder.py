import logging
import time

import pytest

from vrchat_recorder.abc.base_recorder import BaseRecorder


class TestBaseRecorderImpl(BaseRecorder):
    def __init__(self):
        self.data = []

    def record(self):
        self.data.append("test_data")


class TestBaseRecorderImplError(BaseRecorder):
    def record(self):
        raise Exception("test_error")


def test_BaseRecorder(caplog: pytest.LogCaptureFixture):
    caplog.set_level(0)
    # Test record method
    recorder = TestBaseRecorderImpl()
    recorder.record()
    assert recorder.data == ["test_data"]

    # Test background recording
    recorder.record_background()

    # Test logger info when background recording starts
    assert "Started background recording." in caplog.text

    recorder.shutdown()

    # Test logger info when background recording is shut down
    assert "Shutdown background recording." in caplog.text

    # Test error handling in _record_with_error_capture
    recorder = TestBaseRecorderImplError()
    recorder.record_background()
    recorder.shutdown()
    assert "test_error" in caplog.text
