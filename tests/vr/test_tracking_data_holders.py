import pytest

from vrchat_recorder.vr.tracking_data_holders import (
    Axis,
    BothControllerTrackingData,
    ControllerTrackingData,
    Orientation,
    Position,
    TrackingData,
    VRDeviceTrackingDataHolder,
)


def test_position_data_class():
    p = Position(1.0, 2.0, 3.0)
    assert p.x == 1.0
    assert p.y == 2.0
    assert p.z == 3.0


def test_orientation_data_class():
    o = Orientation(1.0, 2.0, 3.0, 4.0)
    assert o.x == 1.0
    assert o.y == 2.0
    assert o.z == 3.0
    assert o.w == 4.0


def test_axis_data_class():
    a = Axis(1.0, 2.0)
    assert a.x == 1.0
    assert a.y == 2.0


def test_tracking_data_class():
    p = Position(1.0, 2.0, 3.0)
    o = Orientation(1.0, 2.0, 3.0, 4.0)
    td = TrackingData(p, o)
    assert td.position == p
    assert td.orientation == o


def test_controller_tracking_data_class():
    p = Position(1.0, 2.0, 3.0)
    o = Orientation(1.0, 2.0, 3.0, 4.0)
    ts = Axis(1.0, 2.0)
    ft = Axis(3.0, 4.0)
    st = Axis(5.0, 6.0)
    tt = Axis(7.0, 8.0)
    ft2 = Axis(9.0, 10.0)
    ctd = ControllerTrackingData(p, o, ts, ft, st, tt, ft2)
    assert ctd.position == p
    assert ctd.orientation == o
    assert ctd.thumb_stick == ts
    assert ctd.first_trigger == ft
    assert ctd.second_trigger == st
    assert ctd.third_trigger == tt
    assert ctd.fourth_trigger == ft2


def test_both_controller_tracking_data_class():
    p1 = Position(1.0, 2.0, 3.0)
    o1 = Orientation(1.0, 2.0, 3.0, 4.0)
    ts1 = Axis(1.0, 2.0)
    ft1 = Axis(3.0, 4.0)
    st1 = Axis(5.0, 6.0)
    tt1 = Axis(7.0, 8.0)
    ft21 = Axis(9.0, 10.0)
    ctd1 = ControllerTrackingData(p1, o1, ts1, ft1, st1, tt1, ft21)

    p2 = Position(11.0, 12.0, 13.0)
    o2 = Orientation(11.0, 12.0, 13.0, 14.0)
    ts2 = Axis(11.0, 12.0)
    ft2 = Axis(13.0, 14.0)
    st2 = Axis(15.0, 16.0)
    tt2 = Axis(17.0, 18.0)
    ft22 = Axis(18.0, 19.0)
    ctd2 = ControllerTrackingData(p2, o2, ts2, ft2, st2, tt2, ft22)

    bctd = BothControllerTrackingData(ctd1, ctd2)
    assert bctd.left == ctd1
    assert bctd.right == ctd2


def test_vr_data_holder_class():
    p1 = Position(1.0, 2.0, 3.0)
    o1 = Orientation(1.0, 2.0, 3.0, 4.0)
    ts1 = Axis(1.0, 2.0)
    ft1 = Axis(3.0, 4.0)
    st1 = Axis(5.0, 6.0)
    tt1 = Axis(7.0, 8.0)
    ft21 = Axis(9.0, 10.0)
    ctd1 = ControllerTrackingData(p1, o1, ts1, ft1, st1, tt1, ft21)

    p2 = Position(11.0, 12.0, 13.0)
    o2 = Orientation(11.0, 12.0, 13.0, 14.0)
    ts2 = Axis(11.0, 12.0)
    ft2 = Axis(13.0, 14.0)
    st2 = Axis(15.0, 16.0)
    tt2 = Axis(17.0, 18.0)
    ft22 = Axis(19.0, 20.0)
    ctd2 = ControllerTrackingData(p2, o2, ts2, ft2, st2, tt2, ft22)

    vr = VRDeviceTrackingDataHolder(123.456, TrackingData(p1, o1), BothControllerTrackingData(ctd1, ctd2))
    assert vr.timestamp == 123.456
    assert vr.hmd.position == p1
    assert vr.hmd.orientation == o1
    assert vr.controller.left.position == p1
    assert vr.controller.left.orientation == o1
    assert vr.controller.left.thumb_stick == ts1
    assert vr.controller.left.first_trigger == ft1
    assert vr.controller.left.second_trigger == st1
    assert vr.controller.left.third_trigger == tt1
    assert vr.controller.left.fourth_trigger == ft21
    assert vr.controller.right.position == p2
    assert vr.controller.right.orientation == o2
    assert vr.controller.right.thumb_stick == ts2
    assert vr.controller.right.first_trigger == ft2
    assert vr.controller.right.second_trigger == st2
    assert vr.controller.right.third_trigger == tt2
    assert vr.controller.right.fourth_trigger == ft22
