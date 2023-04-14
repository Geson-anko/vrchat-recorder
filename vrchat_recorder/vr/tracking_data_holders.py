"""This file contains features for holding tracking data and etc."""

from dataclasses import dataclass


@dataclass
class Position:
    """Position data class."""

    x: float
    y: float
    z: float


@dataclass
class Orientation:
    """Orientation data class."""

    x: float
    y: float
    z: float
    w: float


@dataclass
class Axis:
    """Axis data class."""

    x: float
    y: float


@dataclass
class TrackingData:
    """Tracking data class."""

    position: Position
    orientation: Orientation


@dataclass
class ControllerTrackingData(TrackingData):
    thumb_stick: Axis
    first_trigger: Axis
    second_trigger: Axis
    third_trigger: Axis
    fourth_trigger: Axis


@dataclass
class BothControllerTrackingData:
    """Both controller tracking data class."""

    left: ControllerTrackingData
    right: ControllerTrackingData


@dataclass
class VRDeviceTrackingDataHolder:
    """VR data holder class."""

    timestamp: float
    hmd: TrackingData
    controller: BothControllerTrackingData


def create_empty_data_holder() -> VRDeviceTrackingDataHolder:
    """Creates empty VRDeviceTrackingDataHolder class. All values are initialized with `0.0`.

    Returns:
        VRDeviceTrackingDataHolder: Empty VRDeviceTrackingDataHolder class.
    """

    return VRDeviceTrackingDataHolder(
        timestamp=0.0,
        hmd=TrackingData(position=Position(x=0.0, y=0.0, z=0.0), orientation=Orientation(x=0.0, y=0.0, z=0.0, w=0.0)),
        controller=BothControllerTrackingData(
            left=ControllerTrackingData(
                position=Position(x=0.0, y=0.0, z=0.0),
                orientation=Orientation(x=0.0, y=0.0, z=0.0, w=0.0),
                thumb_stick=Axis(x=0.0, y=0.0),
                first_trigger=Axis(x=0.0, y=0.0),
                second_trigger=Axis(x=0.0, y=0.0),
                third_trigger=Axis(x=0.0, y=0.0),
                fourth_trigger=Axis(x=0.0, y=0.0),
            ),
            right=ControllerTrackingData(
                position=Position(x=0.0, y=0.0, z=0.0),
                orientation=Orientation(x=0.0, y=0.0, z=0.0, w=0.0),
                thumb_stick=Axis(x=0.0, y=0.0),
                first_trigger=Axis(x=0.0, y=0.0),
                second_trigger=Axis(x=0.0, y=0.0),
                third_trigger=Axis(x=0.0, y=0.0),
                fourth_trigger=Axis(x=0.0, y=0.0),
            ),
        ),
    )
