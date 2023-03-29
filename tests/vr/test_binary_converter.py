import struct

from pytest import approx

from vrchat_recorder.vr.binary_converter import (
    binary_format,
    binary_to_holder,
    holder_to_binary,
)
from vrchat_recorder.vr.tracking_data_holders import (
    VRDeviceTrackingDataHolder,
    create_empty_data_holder,
)


def test_holder_to_binary():
    holder = create_empty_data_holder()
    holder.timestamp = 123.456

    # HMD
    holder.hmd.position.x = 1.0
    holder.hmd.position.y = 2.0
    holder.hmd.position.z = 3.0

    holder.hmd.orientation.x = 0.1
    holder.hmd.orientation.y = 0.2
    holder.hmd.orientation.z = 0.3
    holder.hmd.orientation.w = 0.4

    # Left controller
    holder.controller.left.position.x = -1.0
    holder.controller.left.position.y = -2.0
    holder.controller.left.position.z = -3.0

    holder.controller.left.orientation.x = -0.1
    holder.controller.left.orientation.y = -0.2
    holder.controller.left.orientation.z = -0.3
    holder.controller.left.orientation.w = -0.4

    holder.controller.left.thumb_stick.x = 0.5
    holder.controller.left.thumb_stick.y = 0.6

    holder.controller.left.first_trigger.x = 0.7
    holder.controller.left.first_trigger.y = 0.8

    holder.controller.left.second_trigger.x = 0.9
    holder.controller.left.second_trigger.y = 1.0

    holder.controller.left.third_trigger.x = 1.1
    holder.controller.left.third_trigger.y = 1.2

    holder.controller.left.fourth_trigger.x = 1.3
    holder.controller.left.fourth_trigger.y = 1.4

    # Right controller
    holder.controller.right.position.x = 2.0
    holder.controller.right.position.y = 3.0
    holder.controller.right.position.z = 4.0

    holder.controller.right.orientation.x = 0.5
    holder.controller.right.orientation.y = 0.6
    holder.controller.right.orientation.z = 0.7
    holder.controller.right.orientation.w = 0.8

    holder.controller.right.thumb_stick.x = -0.5
    holder.controller.right.thumb_stick.y = -0.6

    holder.controller.right.first_trigger.x = -0.7
    holder.controller.right.first_trigger.y = -0.8

    holder.controller.right.second_trigger.x = -0.9
    holder.controller.right.second_trigger.y = -1.0

    holder.controller.right.third_trigger.x = -1.1
    holder.controller.right.third_trigger.y = -1.2

    holder.controller.right.fourth_trigger.x = -1.3
    holder.controller.right.fourth_trigger.y = -1.4

    binary_data = holder_to_binary(holder)
    assert len(binary_data) == struct.calcsize(binary_format)

    unpacked_data = struct.unpack(binary_format, binary_data)
    assert len(unpacked_data) == 42

    # format: assert unpacked_data[i] == approx(expected)

    assert unpacked_data[0] == approx(123.456)
    assert unpacked_data[1] == approx(1.0)
    assert unpacked_data[2] == approx(2.0)
    assert unpacked_data[3] == approx(3.0)
    assert unpacked_data[4] == approx(0.1)
    assert unpacked_data[5] == approx(0.2)
    assert unpacked_data[6] == approx(0.3)
    assert unpacked_data[7] == approx(0.4)
    assert unpacked_data[8] == approx(-1.0)
    assert unpacked_data[9] == approx(-2.0)
    assert unpacked_data[10] == approx(-3.0)
    assert unpacked_data[11] == approx(-0.1)
    assert unpacked_data[12] == approx(-0.2)
    assert unpacked_data[13] == approx(-0.3)
    assert unpacked_data[14] == approx(-0.4)
    assert unpacked_data[15] == approx(0.5)
    assert unpacked_data[16] == approx(0.6)
    assert unpacked_data[17] == approx(0.7)
    assert unpacked_data[18] == approx(0.8)
    assert unpacked_data[19] == approx(0.9)
    assert unpacked_data[20] == approx(1.0)
    assert unpacked_data[21] == approx(1.1)
    assert unpacked_data[22] == approx(1.2)
    assert unpacked_data[23] == approx(1.3)
    assert unpacked_data[24] == approx(1.4)
    assert unpacked_data[25] == approx(2.0)
    assert unpacked_data[26] == approx(3.0)
    assert unpacked_data[27] == approx(4.0)
    assert unpacked_data[28] == approx(0.5)
    assert unpacked_data[29] == approx(0.6)
    assert unpacked_data[30] == approx(0.7)
    assert unpacked_data[31] == approx(0.8)
    assert unpacked_data[32] == approx(-0.5)
    assert unpacked_data[33] == approx(-0.6)
    assert unpacked_data[34] == approx(-0.7)
    assert unpacked_data[35] == approx(-0.8)
    assert unpacked_data[36] == approx(-0.9)
    assert unpacked_data[37] == approx(-1.0)
    assert unpacked_data[38] == approx(-1.1)
    assert unpacked_data[39] == approx(-1.2)
    assert unpacked_data[40] == approx(-1.3)
    assert unpacked_data[41] == approx(-1.4)


def test_binary_to_holder():
    binary_data = struct.pack(
        binary_format,
        123.456,
        1.0,
        2.0,
        3.0,
        0.1,
        0.2,
        0.3,
        0.4,
        -1.0,
        -2.0,
        -3.0,
        -0.1,
        -0.2,
        -0.3,
        -0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
        1.1,
        1.2,
        1.3,
        1.4,
        2.0,
        3.0,
        4.0,
        0.5,
        0.6,
        0.7,
        0.8,
        -0.5,
        -0.6,
        -0.7,
        -0.8,
        -0.9,
        -1.0,
        -1.1,
        -1.2,
        -1.3,
        -1.4,
    )

    holder = binary_to_holder(binary_data)
    assert isinstance(holder, VRDeviceTrackingDataHolder)

    assert holder.timestamp == approx(123.456)

    # HMD
    assert holder.hmd.position.x == approx(1.0)
    assert holder.hmd.position.y == approx(2.0)
    assert holder.hmd.position.z == approx(3.0)

    assert holder.hmd.orientation.x == approx(0.1)
    assert holder.hmd.orientation.y == approx(0.2)
    assert holder.hmd.orientation.z == approx(0.3)
    assert holder.hmd.orientation.w == approx(0.4)

    # Left controller
    assert holder.controller.left.position.x == approx(-1.0)
    assert holder.controller.left.position.y == approx(-2.0)
    assert holder.controller.left.position.z == approx(-3.0)

    assert holder.controller.left.orientation.x == approx(-0.1)
    assert holder.controller.left.orientation.y == approx(-0.2)
    assert holder.controller.left.orientation.z == approx(-0.3)
    assert holder.controller.left.orientation.w == approx(-0.4)

    assert holder.controller.left.thumb_stick.x == approx(0.5)
    assert holder.controller.left.thumb_stick.y == approx(0.6)

    assert holder.controller.left.first_trigger.x == approx(0.7)
    assert holder.controller.left.first_trigger.y == approx(0.8)

    assert holder.controller.left.second_trigger.x == approx(0.9)
    assert holder.controller.left.second_trigger.y == approx(1.0)

    assert holder.controller.left.third_trigger.x == approx(1.1)
    assert holder.controller.left.third_trigger.y == approx(1.2)

    assert holder.controller.left.fourth_trigger.x == approx(1.3)
    assert holder.controller.left.fourth_trigger.y == approx(1.4)

    # Right controller
    assert holder.controller.right.position.x == approx(2.0)
    assert holder.controller.right.position.y == approx(3.0)
    assert holder.controller.right.position.z == approx(4.0)

    assert holder.controller.right.orientation.x == approx(0.5)
    assert holder.controller.right.orientation.y == approx(0.6)
    assert holder.controller.right.orientation.z == approx(0.7)
    assert holder.controller.right.orientation.w == approx(0.8)

    assert holder.controller.right.thumb_stick.x == approx(-0.5)
    assert holder.controller.right.thumb_stick.y == approx(-0.6)

    assert holder.controller.right.first_trigger.x == approx(-0.7)
    assert holder.controller.right.first_trigger.y == approx(-0.8)

    assert holder.controller.right.second_trigger.x == approx(-0.9)
    assert holder.controller.right.second_trigger.y == approx(-1.0)

    assert holder.controller.right.third_trigger.x == approx(-1.1)
    assert holder.controller.right.third_trigger.y == approx(-1.2)

    assert holder.controller.right.fourth_trigger.x == approx(-1.3)
    assert holder.controller.right.fourth_trigger.y == approx(-1.4)
