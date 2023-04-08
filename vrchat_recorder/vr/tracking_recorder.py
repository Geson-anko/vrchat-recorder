"""This file contains TrackingRecorder class that records vr tracking data continuously."""

import json
import logging
import time
from typing import BinaryIO, List

import numpy as np
import openvr
from scipy.spatial.transform import Rotation

from ..abc.base_recorder import BaseRecorder
from .binary_converter import binary_format, holder_to_binary
from .constants import HeaderNames, HeaderVersions
from .tracking_data_holders import Axis, Orientation, Position, create_empty_data_holder

logger = logging.getLogger(__name__)


class TrackingRecorder(BaseRecorder):
    """This class records vr tracking data continuously.

    Usage:
        ```python
        from vrchat_recorder.vr.tracking_recorder import TrackingRecorder

        tr = TrackingRecorder("path/to/file.bin", frame_rate=60)
        tr.record()
        ```

    Recording data:
        - timestamp
        - hmd position
        - hmd orientation
        - controller position
        - controller orientation
        - controller thumb stick
        - controller triggers (first to fourth).

    You can see binary format in `vrchat_recorder.vr.binary_converter.binary_format`.

    Header is written at the beginning of the file, and json format is used.
    Structure of the header is can be seen `create_header` function.
    """

    def __init__(
        self,
        output_file_path: str,
        vrsystem: openvr.IVRSystem,
        frame_rate: int = 72,
        num_frames_per_flush: int = 1000,
    ):
        """Initialize TrackingRecorder.

        Args:
            output_file_path (str): Path to save file.
            vr_system (openvr.IVRSystem): OpenVR system object.
            frame_rate (int): Frame rate to record. Defaults to 72.
            num_frames_per_flush (int): Number of frames to record before flushing to disk.
        """
        self.output_file_path = output_file_path
        self.vrsystem = vrsystem
        self.frame_rate = frame_rate
        self.num_frames_per_flush = num_frames_per_flush
        self._holder = create_empty_data_holder()

    def _update_timestamp(self) -> None:
        """Update the timestamp in the data holder."""
        self._holder.timestamp = time.time()

    def _get_device_poses(self) -> List[openvr.TrackedDevicePose_t]:
        """Get the device poses from the VR system.

        Returns:
            List[openvr.TrackedDevicePose_t]: A list containing the poses of all tracked devices.
        """

        poses = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
        device_poses = poses()
        self.vrsystem.getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, device_poses)
        return device_poses

    def _update_data_holder(self, device_poses: List[openvr.TrackedDevicePose_t]) -> None:
        """Update the data holder with the device poses.

        Args:
            device_poses (List[openvr.TrackedDevicePose_t]): A list containing the poses of all tracked devices.
        """

        for device_index in range(openvr.k_unMaxTrackedDeviceCount):
            device_class = self.vrsystem.getTrackedDeviceClass(device_index)
            device_pose = device_poses[device_index]

            if device_pose.bDeviceIsConnected:
                pose_matrix = np.zeros((3, 4), dtype=float)
                pose_matrix[:] = device_pose.mDeviceToAbsoluteTracking
                position = pose_matrix[:3, 3]
                rotation = Rotation.from_matrix(pose_matrix[:3, :3])
                quaternion = rotation.as_quat()

                if device_class == openvr.TrackedDeviceClass_HMD:
                    self._holder.hmd.position = Position(position[0], position[1], position[2])
                    self._holder.hmd.orientation = Orientation(
                        quaternion[0], quaternion[1], quaternion[2], quaternion[3]
                    )

                elif device_class == openvr.TrackedDeviceClass_Controller:
                    controller_role = self.vrsystem.getControllerRoleForTrackedDeviceIndex(device_index)
                    state = self.vrsystem.getControllerState(device_index)[1]
                    if controller_role == openvr.TrackedControllerRole_LeftHand:
                        self._holder.controller.left.position = Position(position[0], position[1], position[2])
                        self._holder.controller.left.orientation = Orientation(
                            quaternion[0], quaternion[1], quaternion[2], quaternion[3]
                        )
                        self._holder.controller.left.thumb_stick = Axis(state.rAxis[0].x, state.rAxis[0].y)
                        self._holder.controller.left.first_trigger = Axis(state.rAxis[1].x, state.rAxis[1].y)
                        self._holder.controller.left.second_trigger = Axis(state.rAxis[2].x, state.rAxis[2].y)
                        self._holder.controller.left.third_trigger = Axis(state.rAxis[3].x, state.rAxis[3].y)
                        self._holder.controller.left.fourth_trigger = Axis(state.rAxis[4].x, state.rAxis[4].y)

                    elif controller_role == openvr.TrackedControllerRole_RightHand:
                        self._holder.controller.right.position = Position(position[0], position[1], position[2])
                        self._holder.controller.right.orientation = Orientation(
                            quaternion[0], quaternion[1], quaternion[2], quaternion[3]
                        )
                        self._holder.controller.right.thumb_stick = Axis(state.rAxis[0].x, state.rAxis[0].y)
                        self._holder.controller.right.first_trigger = Axis(state.rAxis[1].x, state.rAxis[1].y)
                        self._holder.controller.right.second_trigger = Axis(state.rAxis[2].x, state.rAxis[2].y)
                        self._holder.controller.right.third_trigger = Axis(state.rAxis[3].x, state.rAxis[3].y)
                        self._holder.controller.right.fourth_trigger = Axis(state.rAxis[4].x, state.rAxis[4].y)

    @staticmethod
    def _write_header(outfile: BinaryIO) -> None:
        """Write the header to the output file.

        Args:
            outfile (BinaryIO): The output file to write the header to.
        """
        header = create_header()
        header_size = len(header)
        outfile.write(header_size.to_bytes(4, byteorder="little"))
        outfile.write(header)

    def _write_binary_data(self, outfile: BinaryIO, frame_count: int) -> int:
        """Write the binary data to the output file and update the frame count.

        Args:
            outfile (BinaryIO): The output file to write the binary data to.
            frame_count (int): The current frame count.

        Returns:
            int: The updated frame count.
        """
        binary = holder_to_binary(self._holder)
        outfile.write(binary)
        frame_count += 1

        if frame_count % self.num_frames_per_flush == 0:
            outfile.flush()
            frame_count = 0

        return frame_count

    def record(self) -> None:
        """Record data to the output file until Keyboard interrupt or shutdown.

        You can quit the recording by pressing Ctrl+C or `self.shutdown()`(setting `self._shutdown` to True).
        """
        logger.info(f"VR Tracking Recorder started. Output to {self.output_file_path}")

        self._shutdown = False
        frame_count = 0
        self._holder = create_empty_data_holder()

        try:
            with open(self.output_file_path, "wb") as outfile:

                self._write_header(outfile)

                while self._shutdown is False:

                    if (time.time() - self._holder.timestamp) < (1 / self.frame_rate):
                        time.sleep(1 / self.frame_rate - (time.time() - self._holder.timestamp))

                    self._update_timestamp()
                    device_poses = self._get_device_poses()
                    self._update_data_holder(device_poses)
                    frame_count = self._write_binary_data(outfile, frame_count)

        except KeyboardInterrupt:
            pass

        logger.info("VR Tracking Recorder stopped.")


def create_header() -> bytes:
    """Create the header for the output file.

    Returns:
        bytes: The header.
    """

    header = {
        HeaderNames.VERSION: HeaderVersions.V0,
        HeaderNames.BINARY_FORMAT: binary_format,
    }

    return json.dumps(header).encode("utf-8")
