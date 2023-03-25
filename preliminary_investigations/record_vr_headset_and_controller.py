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

        for device_index in range(openvr.k_unMaxTrackedDeviceCount):
            device_class = system.getTrackedDeviceClass(device_index)
            device_pose = device_poses[device_index]

            if device_pose.bDeviceIsConnected:
                pose_matrix = convert_matrix34_to_matrix44(device_pose.mDeviceToAbsoluteTracking)
                position = pose_matrix[:3, 3]
                rotation = Rotation.from_matrix(pose_matrix[:3, :3])
                orientation = rotation.as_quat()

                if device_class == openvr.TrackedDeviceClass_HMD:
                    print(f"Headset - Position: {position}, Orientation: {orientation}")
                elif device_class == openvr.TrackedDeviceClass_Controller:
                    controller_role = system.getControllerRoleForTrackedDeviceIndex(device_index)
                    if controller_role == openvr.TrackedControllerRole_LeftHand:
                        print(f"Left Controller - Position: {position}, Orientation: {orientation}")
                    elif controller_role == openvr.TrackedControllerRole_RightHand:
                        print(f"Right Controller - Position: {position}, Orientation: {orientation}")

        # Sleep for a while to avoid high CPU usage
        time.sleep(0.1)

    except KeyboardInterrupt:
        running = False

# Clean up
openvr.shutdown()
