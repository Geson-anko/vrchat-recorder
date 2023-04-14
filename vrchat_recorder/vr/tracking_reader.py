"""This file contains TrackingReader class that reads vr tracking data."""

import json
import struct
from typing import Optional

from .binary_converter import binary_to_holder
from .constants import HeaderNames, HeaderVersions
from .tracking_data_holders import VRDeviceTrackingDataHolder


class TrackingReader:
    """This class reads vr tracking data.

    Usage:
        ```python
        from vrchat_recorder.vr.tracking_readerer import TrackingReader

        tr = TrackingReader("path/to/file.bin")
        data_holder = tr.read() # read a frame.
        ```
    You can get stored frame num by `num_frames` property,
    and current count of read frames by `read_count` property.
    You can see binary format in `vrchat_recorder.vr.binary_converter.binary_format`.
    """

    def __init__(self, input_file_path: str) -> None:
        """Initialize TrackingReader.

        Args:
            input_file_path (str): Path to read file.
        """
        self.input_file_path = input_file_path
        self._file = open(input_file_path, "rb")
        header_size, header = self.get_header()
        if header[HeaderNames.VERSION] != HeaderVersions.V0:
            raise ValueError("Invalid header version.")

        binary_format = header[HeaderNames.BINARY_FORMAT]

        self._binary_format = binary_format
        self._header_size = header_size
        self._header_size_with_initial = header_size + 4

        self._binary_size = struct.calcsize(binary_format)
        self._num_frames = (self._file.seek(0, 2) - self._header_size_with_initial) // self._binary_size
        self._count = 0

        self.reset()

    @property
    def num_frames(self) -> int:
        """Returns the number of frames in the file."""
        return self._num_frames

    @property
    def read_count(self) -> int:
        """Returns the number of frames read."""
        return self._count

    def get_header(self) -> tuple[int, dict]:
        """Get header information from file.

        Returns:
            int: Header size.
            dict: Header information.
        """

        self._file.seek(0)
        header_size = int.from_bytes(self._file.read(4), "little")
        header = json.loads(self._file.read(header_size).decode("utf-8"))
        return header_size, header

    def reset(self):
        """Resets file pointer to the beginning of the file."""
        self._file.seek(self._header_size_with_initial)
        self._count = 0

    def read(self) -> Optional[VRDeviceTrackingDataHolder]:
        """Reads a vr tracking data. If EOF, returns None.

        Returns:
            VRDeviceTrackingDataHolder: DataHolder class.
        """
        binary = self._file.read(self._binary_size)
        if not binary:
            return None
        self._holder = binary_to_holder(binary)
        self._count += 1
        return self._holder

    def close(self):
        """Closes file."""
        self._file.close()

    def __del__(self):
        self.close()

    def __repr__(self):
        return f"{self.__class__.__name__}(input_file_path={self.input_file_path},)"
