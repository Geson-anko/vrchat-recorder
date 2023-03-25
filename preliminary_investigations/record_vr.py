import time

import numpy as np
import openvr
from scipy.spatial.transform import Rotation


def convert_matrix34_to_matrix44(matrix34):
    matrix44 = np.eye(4, dtype=np.float32)
    matrix44[:3, :] = matrix34
    return matrix44


# Initialize OpenVR
openvr.init(openvr.VRApplication_Background)

# Get the system
system = openvr.VRSystem()

# Main loop
running = True
while running:
    try:
        # Get the device pose
        poses = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
        device_poses = poses()
        system.getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, device_poses)

        # Get the headset pose
        headset_pose = device_poses[openvr.k_unTrackedDeviceIndex_Hmd]

        # Check if the headset is connected
        if headset_pose.bDeviceIsConnected:
            # Get the position and orientation (in a 3x4 matrix)
            pose_matrix = convert_matrix34_to_matrix44(headset_pose.mDeviceToAbsoluteTracking)

            # Extract position
            position = pose_matrix[:3, 3]

            # Extract orientation (as a quaternion)
            rotation = Rotation.from_matrix(pose_matrix[:3, :3])
            orientation = rotation.as_quat()

            # Print position and orientation
            print(f"Position: {position}, Orientation: {orientation}")

        # Sleep for a while to avoid high CPU usage
        time.sleep(0.1)

    except KeyboardInterrupt:
        running = False

# Clean up
openvr.shutdown()
