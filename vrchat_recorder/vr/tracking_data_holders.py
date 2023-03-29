"""This file contains features for holding tracking data and etc."""

from dataclasses import dataclass


@dataclass
class Position:
    """Position data class."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Orientation:
    """Orientation data class."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 0.0


@dataclass
class Axis:
    """Axis data class."""

    x: float = 0.0
    y: float = 0.0


@dataclass
class TrackingData:
    """Tracking data class."""

    position: Position = Position()
    orientation: Orientation = Orientation()


@dataclass
class ControllerTrackingData(TrackingData):
    thumb_stick: Axis = Axis()
    first_trigger: Axis = Axis()
    second_trigger: Axis = Axis()
    third_trigger: Axis = Axis()
    fourth_trigger: Axis = Axis()


@dataclass
class BothControllerTrackingData:
    """Both controller tracking data class."""

    left: ControllerTrackingData = ControllerTrackingData()
    right: ControllerTrackingData = ControllerTrackingData()


@dataclass
class VRDeviceTrackingDataHolder:
    """VR data holder class."""

    timestamp: float = 0.0
    hmd: TrackingData = TrackingData()
    controller: BothControllerTrackingData = BothControllerTrackingData()
