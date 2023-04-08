"""This file contains the ControllerEventRecorder class that records controller events."""

import csv
import logging
import time
from typing import TextIO

import openvr

from ..abc.csv_recorder import CSVRecorder
from ..data_constants import CSVHeaderNames as HN

logger = logging.getLogger(__name__)


class ControllerEventRecorder(CSVRecorder):
    """ControllerEventRecorder records controller events.

    Usage:
        ```python
        from vrchat_recorder.vr.event_recorder import ControllerEventRecorder

        vrsystem = openvr.init(openvr.VRApplication_Background)
        er = ControllerEventRecorder("path/to/file.csv", vrsystem)
        er.record()
        ```
    """

    def __init__(
        self,
        output_file_path: str,
        vrsystem: openvr.IVRSystem,
        poll_interval: float = 0.001,
        flush_interval: float = 10.0,
    ) -> None:
        """Initialize ControllerEventRecorder.

        Args:
            output_file_path (str): Path to save file.
            vrsystem (openvr.IVRSystem): OpenVR system object.
            poll_interval (float): Interval to poll controller events.
            flush_interval (float): Interval to flush file.
        """
        csv_headers = [
            HN.TIMESTAMP,
            HN.EVENT_TYPE,
            HN.CONTROLLER_ROLE,
            HN.BUTTON_ID,
            HN.AGE_SECONDS,
        ]
        super().__init__(output_file_path, csv_headers)
        self.vrsystem = vrsystem
        self.poll_interval = poll_interval
        self.flush_interval = flush_interval

    def record(self) -> None:
        """Record data to the output file until Keyboard interrupt or shutdown."""
        logger.info(f"Recording controller events to {self.output_file_path}...")

        with open(self.output_file_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_headers)
            previous_flush = time.time()

            try:
                while not self._shutdown:
                    self._record_controller_events(writer)
                    previous_flush = self._flush_file_if_needed(csvfile, previous_flush)
                    time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                pass

        logger.info("Recording finished.")

    def _record_controller_events(self, writer: csv.DictWriter) -> None:
        """Record controller events if any.

        Args:
            writer (csv.DictWriter): CSV writer object.
        """
        event = openvr.VREvent_t()

        while self.vrsystem.pollNextEvent(event):
            timestamp = time.time()
            if self._is_controller_event(event):
                data = self._extract_event_data(event, timestamp)
                writer.writerow(data)

    def _is_controller_event(self, event: openvr.VREvent_t) -> bool:
        """Check if the given event is a controller event.

        Args:
            event (openvr.VREvent_t): Event to check.
        """
        device_index = event.trackedDeviceIndex
        device_class = self.vrsystem.getTrackedDeviceClass(device_index)

        if device_class == openvr.TrackedDeviceClass_Controller:
            event_type = event.eventType

            if event_type in [
                openvr.VREvent_ButtonPress,
                openvr.VREvent_ButtonUnpress,
                openvr.VREvent_ButtonTouch,
                openvr.VREvent_ButtonUntouch,
            ]:
                return True

        return False

    def _extract_event_data(self, event: openvr.VREvent_t, timestamp: float) -> dict:
        """Extract event data from the given event.

        Args:
            event (openvr.VREvent_t): Event to extract data from.
            timestamp (float): Timestamp of the event.
        """
        device_index = event.trackedDeviceIndex
        controller_role = self.vrsystem.getControllerRoleForTrackedDeviceIndex(device_index)
        event_type = event.eventType
        button_id = event.data.controller.button
        age_seconds = event.eventAgeSeconds

        return {
            HN.TIMESTAMP: timestamp,
            HN.EVENT_TYPE: event_type,
            HN.CONTROLLER_ROLE: controller_role,
            HN.BUTTON_ID: button_id,
            HN.AGE_SECONDS: age_seconds,
        }

    def _flush_file_if_needed(self, csvfile: TextIO, previous_flush: float) -> float:
        """Flush data to the file if the flush interval has passed.

        Args:
            csvfile (file): File object.
            previous_flush (float): Timestamp of the previous flush.

        Returns:
            float: Timestamp of the current flush.
        """
        if self.flush_interval < time.time() - previous_flush:
            csvfile.flush()
            previous_flush = time.time()

        return previous_flush
