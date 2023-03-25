"""This file contains abstract classes for recording data."""

import logging
import threading
from abc import ABC, abstractmethod
from typing import Optional

logger = logging.getLogger(__name__)


class BaseRecorder(ABC):
    """This is an abstract class for recording data.

    Recording can be backgrounded by using threading. You can shutdown the background recording by `self.shutdown`
    (setting `self._shutdown` to True).
    """

    _shutdown: bool = False
    backgroud_thread: Optional[threading.Thread] = None

    @abstractmethod
    def record(self):
        """Record data to the output file."""
        pass

    def _record_with_error_capture(self):
        """Record data to the output file with error capture."""
        try:
            self.record()
        except Exception as e:
            logger.exception(e)

    def record_background(self):
        """Record data to the output file in background."""
        self._shutdown = False
        self.backgroud_thread = threading.Thread(target=self._record_with_error_capture)
        self.backgroud_thread.start()
        logger.debug("Started background recording.")

    def shutdown(self):
        """Shutdown the background recording."""

        self._shutdown = True
        if self.backgroud_thread is not None:
            self.backgroud_thread.join()
            logger.debug("Shutdown background recording.")
