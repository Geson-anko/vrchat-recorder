"""This file contains video recorder class with OBS remote controlling."""

import shutil
import time

import obsws_python as obs

from .abc.base_recorder import BaseRecorder


class OBSVideoRecorder(BaseRecorder):
    """This class records video with OBS remote controlling."""

    def __init__(self, output_file_path: str, host: str, port: int, password: str, wait_interval: float = 0.1):
        """Create an OBSVideoRecorder object.

        Args:
            output_file_path (str): The path to the output file. Do not contain file extension.
            host (str): The IP address of the OBS websocket server.
            port (int): The port of the OBS websocket server.
            password (str): The password of the OBS websocket server.
            wait_interval (float): The interval to wait before checking the shutdown flag.
        """

        self.output_file_path = output_file_path
        self.host = host
        self.port = port
        self.password = password
        self.wait_interval = wait_interval

        self.client = obs.ReqClient(host=host, port=port, password=password)

    def record(self):
        """Record video to the output file until Keyboard interrupt or shutdown.

        You can quit the recording by pressing Ctrl+C or `self.shutdown()` (setting `self._shutdown` to True).
        """
        self.client.start_record()
        try:
            while not self._shutdown:
                time.sleep(self.wait_interval)
        except KeyboardInterrupt:
            pass

        video_path = self.client.stop_record().output_path
        ext = video_path.rsplit(".", 1)[-1]
        output_path = ".".join([self.output_file_path, ext])
        time.sleep(1.0)
        shutil.move(video_path, output_path)
