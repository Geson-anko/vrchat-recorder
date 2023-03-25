"""This file contains the tool for recording OSC feedback data from VRChat."""
import csv
import logging
import threading
import time
from typing import Any, Optional

from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher

from .abc.csv_recorder import CSVRecorder as ABC_CSVRecorder
from .data_constants import CSVHeaderNames as HN
from .data_constants import get_data_type_name

logger = logging.getLogger(__name__)


class OSCFeedbackRecorder(ABC_CSVRecorder):
    """Records OSC feedback data from VRChat to a csv file.
    Usage:
        ```python
        from vrchat_recorder.osc_feedback_recorder import OSCFeedbackRecorder

        ofr = OSCFeedbackRecorder("path/to/output/file.csv", "localhost", 9001, "/avatar/parameters/*")
        ofr.record_background()
        ```
    """

    def __init__(self, output_file_path: Any, host: Any, port: int, address: Any, timeout: float = 1.0) -> None:
        """Create a OSCFeedbackRecorder object.

        Args:
            output_file_path (Any): The path to the output file.
            host (Any): The IP address of the VRChat OSC server.
            port (int): The port of the VRChat OSC server.
            address (Any): The OSC address to record.
            timeout (float): The timeout for the OSC server.
        """

        csv_headers = [HN.TIMESTAMP, HN.PARAMETER_NAME, HN.DATA_TYPE, HN.VALUE]
        super().__init__(output_file_path, csv_headers)

        self.host = host
        self.port = port
        self.address = address
        self.timeout = timeout

    csv_writer: Optional[csv.DictWriter] = None
    server_thread: Optional[threading.Thread] = None

    def record(self):
        """Record data to the output file until Keyboard interrupt or shutdown.

        You can quit the recording by pressing Ctrl+C or `self.shutdown()` (setting `self._shutdown` to True).
        """
        with open(self.output_file_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_headers)
            self.csv_writer = writer
            dispatcher = Dispatcher()
            dispatcher.map(self.address, self._osc_callback)
            server = osc_server.ThreadingOSCUDPServer((self.host, self.port), dispatcher)
            server.timeout = self.timeout
            try:
                while self._shutdown is False:
                    server.handle_request()
            except KeyboardInterrupt:
                pass

    def _osc_callback(self, address, value: Any):
        """Callback function for receiving OSC data.

        Args:
            address (str): The parameter address of OSC.
            value (Any): The value of the parameter.
        """
        timestamp = time.time()
        if self.csv_writer is None:
            logger.warning("CSV writer is not set.")
            return

        self.csv_writer.writerow(
            {
                HN.TIMESTAMP: timestamp,
                HN.PARAMETER_NAME: address,
                HN.DATA_TYPE: get_data_type_name(value),
                HN.VALUE: value,
            }
        )
