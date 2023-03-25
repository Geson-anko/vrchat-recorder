"""This file contains abstract classes for recording data with csv format."""

import csv
import logging
import os
import threading
from abc import ABC, abstractmethod
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CSVRecorder(ABC):
    """This is an abstract class for recording data with csv format.

    Recording can be backgrounded by using threading. You can shutdown the background recording by `self.shutdown`
    (setting `self._shutdown` to True).
    """

    _shutdown: bool = False
    backgroud_thread: Optional[threading.Thread] = None

    def __init__(self, output_file_path: Any, csv_headers: list[str] = None):
        """Create a CSVRecorder object. If the output file exists, warning message will be shown and when its csv header
        is different from the given csv header, ValueError will be raised.

        Args:
            output_file_path (Any): The path to the output file.
            csv_headers (Optional[list[str]]): The csv header.

        Raises:
            ValueError: The csv header of the output file is different from the given csv header.
        """

        if os.path.exists(output_file_path):
            logger.warning(f"Output file already exists: {output_file_path}")
            with open(output_file_path) as f:
                reader = csv.reader(f)
                header = next(reader)
                if csv_headers is not None and header != csv_headers:
                    raise ValueError(
                        f"CSV header of the output file is different from the given csv header: {header} != {csv_headers}"
                    )

        elif csv_headers is not None:
            with open(output_file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(csv_headers)

        self.output_file_path = output_file_path

    @abstractmethod
    def record(self):
        """Record data to the output file."""
        pass

    def record_background(self):
        """Record data to the output file in background."""
        self._shutdown = False
        self.backgroud_thread = threading.Thread(target=self.record)
        self.backgroud_thread.start()
        logger.info(f"Started background recording: {self.output_file_path}")

    def shutdown(self):
        """Shutdown the background recording."""

        self._shutdown = True
        if self.backgroud_thread is not None:
            self.backgroud_thread.join()
            logger.info(f"Shutdown background recording: {self.output_file_path}")
