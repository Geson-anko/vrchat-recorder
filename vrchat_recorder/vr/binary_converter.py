"""This file contains features that converts DataHolder class to binary data."""
import struct
from typing import Optional

from .tracking_data_holders import VRDeviceTrackingDataHolder, create_empty_data_holder

binary_format = " ".join(
    [
        "d",  # timestamp
        "fff",  # hmd position
        "ffff",  # hmd orientation
        "fff",  # left controller position
        "ffff",  # left controller orientation
        "ff",  # left controller thumb stick
        "ff",  # left controller first trigger
        "ff",  # left controller second trigger
        "ff",  # left controller third trigger
        "ff",  # left controller fourth trigger
        "fff",  # right controller position
        "ffff",  # right controller orientation
        "ff",  # right controller thumb stick
        "ff",  # right controller first trigger
        "ff",  # right controller second trigger
        "ff",  # right controller third trigger
        "ff",  # right controller fourth trigger
    ]
)


def holder_to_binary(holder: VRDeviceTrackingDataHolder) -> bytes:
    """Converts DataHolder class to binary data.

    Args:
        holder (VRDeviceTrackingDataHolder): DataHolder class.

    Returns:
        bytes: Binary data.
    """

    data = [
        holder.timestamp,
        # HMD
        holder.hmd.position.x,
        holder.hmd.position.y,
        holder.hmd.position.z,
        holder.hmd.orientation.x,
        holder.hmd.orientation.y,
        holder.hmd.orientation.z,
        holder.hmd.orientation.w,
        # Controllers
        # Left
        holder.controller.left.position.x,
        holder.controller.left.position.y,
        holder.controller.left.position.z,
        holder.controller.left.orientation.x,
        holder.controller.left.orientation.y,
        holder.controller.left.orientation.z,
        holder.controller.left.orientation.w,
        holder.controller.left.thumb_stick.x,
        holder.controller.left.thumb_stick.y,
        holder.controller.left.first_trigger.x,
        holder.controller.left.first_trigger.y,
        holder.controller.left.second_trigger.x,
        holder.controller.left.second_trigger.y,
        holder.controller.left.third_trigger.x,
        holder.controller.left.third_trigger.y,
        holder.controller.left.fourth_trigger.x,
        holder.controller.left.fourth_trigger.y,
        # Right
        holder.controller.right.position.x,
        holder.controller.right.position.y,
        holder.controller.right.position.z,
        holder.controller.right.orientation.x,
        holder.controller.right.orientation.y,
        holder.controller.right.orientation.z,
        holder.controller.right.orientation.w,
        holder.controller.right.thumb_stick.x,
        holder.controller.right.thumb_stick.y,
        holder.controller.right.first_trigger.x,
        holder.controller.right.first_trigger.y,
        holder.controller.right.second_trigger.x,
        holder.controller.right.second_trigger.y,
        holder.controller.right.third_trigger.x,
        holder.controller.right.third_trigger.y,
        holder.controller.right.fourth_trigger.x,
        holder.controller.right.fourth_trigger.y,
    ]
    return struct.pack(binary_format, *data)


def binary_to_holder(binary: bytes, dst: Optional[VRDeviceTrackingDataHolder] = None) -> VRDeviceTrackingDataHolder:
    """Converts binary data to DataHolder class.

    Args:
        binary (bytes): Binary data. Format is defined in `binary_format` variable.
        dst (Optional[VRDeviceTrackingDataHolder], optional): Destination DataHolder class. Defaults to None.

    Returns:
        VRDeviceTrackingDataHolder: DataHolder class.
    """

    binary = struct.unpack(binary_format, binary)
    if dst is None:
        holder = create_empty_data_holder()
    else:
        holder = dst

    holder.timestamp = binary[0]

    # HMD
    holder.hmd.position.x = binary[1]
    holder.hmd.position.y = binary[2]
    holder.hmd.position.z = binary[3]

    holder.hmd.orientation.x = binary[4]
    holder.hmd.orientation.y = binary[5]
    holder.hmd.orientation.z = binary[6]
    holder.hmd.orientation.w = binary[7]

    # Left controller
    holder.controller.left.position.x = binary[8]
    holder.controller.left.position.y = binary[9]
    holder.controller.left.position.z = binary[10]

    holder.controller.left.orientation.x = binary[11]
    holder.controller.left.orientation.y = binary[12]
    holder.controller.left.orientation.z = binary[13]
    holder.controller.left.orientation.w = binary[14]

    holder.controller.left.thumb_stick.x = binary[15]
    holder.controller.left.thumb_stick.y = binary[16]

    holder.controller.left.first_trigger.x = binary[17]
    holder.controller.left.first_trigger.y = binary[18]

    holder.controller.left.second_trigger.x = binary[19]
    holder.controller.left.second_trigger.y = binary[20]

    holder.controller.left.third_trigger.x = binary[21]
    holder.controller.left.third_trigger.y = binary[22]

    holder.controller.left.fourth_trigger.x = binary[23]
    holder.controller.left.fourth_trigger.y = binary[24]

    # Right controller
    holder.controller.right.position.x = binary[25]
    holder.controller.right.position.y = binary[26]
    holder.controller.right.position.z = binary[27]

    holder.controller.right.orientation.x = binary[28]
    holder.controller.right.orientation.y = binary[29]
    holder.controller.right.orientation.z = binary[30]
    holder.controller.right.orientation.w = binary[31]

    holder.controller.right.thumb_stick.x = binary[32]
    holder.controller.right.thumb_stick.y = binary[33]

    holder.controller.right.first_trigger.x = binary[34]
    holder.controller.right.first_trigger.y = binary[35]

    holder.controller.right.second_trigger.x = binary[36]
    holder.controller.right.second_trigger.y = binary[37]

    holder.controller.right.third_trigger.x = binary[38]
    holder.controller.right.third_trigger.y = binary[39]

    holder.controller.right.fourth_trigger.x = binary[40]
    holder.controller.right.fourth_trigger.y = binary[41]

    return holder
