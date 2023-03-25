"""This file contains the tool for recording gamepad data."""

import csv
from typing import Any

import inputs

from .abc.csv_recorder import CSVRecorder as ABC_CSVRecorder
from .data_constants import CSVHeaderNames as HN
from .data_constants import get_data_type_name


class GamepadRecorder(ABC_CSVRecorder):
    """Records gamepad data to a csv file.
    Usage:
    ```python
    from vrchat_recorder.gamepad_recorder import GamepadRecorder

    gpr = GamepadRecorder("path/to/output/file.csv")
    gpr.record_background()
    """

    def __init__(self, output_file_path: Any) -> None:
        """Create a GamepadRecorder object.

        Args:
            output_file_path (Any): The path to the output file.
        """
        csv_headers = [HN.TIMESTAMP, HN.EVENT_TYPE, HN.PARAMETER_NAME, HN.DATA_TYPE, HN.VALUE]
        super().__init__(output_file_path, csv_headers)

    def record(self) -> None:
        """Record data to the output file until Keyboard interrupt or shutdown.

        You can quit the recording by pressing Ctrl+C or setting `self._shutdown` to True. If recording process does not
        terminate in background process, please move some button or stick for passing `get_gamepad()` function.
        """

        with open(self.output_file_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_headers)
            try:
                while self._shutdown is False:
                    events = inputs.get_gamepad()
                    for event in events:
                        writer.writerow(
                            {
                                HN.TIMESTAMP: event.timestamp,
                                HN.EVENT_TYPE: event.ev_type,
                                HN.PARAMETER_NAME: event.code,
                                HN.DATA_TYPE: get_data_type_name(event.state),
                                HN.VALUE: event.state,
                            }
                        )

            except KeyboardInterrupt:
                pass
