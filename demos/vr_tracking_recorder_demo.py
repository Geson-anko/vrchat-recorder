"""This demostrations how to use TrackingRecorder class.
After start recording in background, you can see HMD position, orientation and etc.
The console outputs the following while being overwritten.

---
timestamp: 1610000000.0
HMD position: Position(x=0.0, y=0.0, z=0.0)
HMD orientation: Orientation(x=0.0, y=0.0, z=0.0, w=0.0)

Controller left position: Position(x=0.0, y=0.0, z=0.0)
Controller left orientation: Orientation(x=0.0, y=0.0, z=0.0, w=0.0)
Controller left thumb stick: Axis(x=0.0, y=0.0)
Controller left first trigger: Axis(x=0.0, y=0.0)
Controller left second trigger: Axis(x=0.0, y=0.0)

Controller right position: Position(x=0.0, y=0.0, z=0.0)
Controller right orientation: Orientation(x=0.0, y=0.0, z=0.0, w=0.0)
Controller right thumb stick: Axis(x=0.0, y=0.0)
Controller right first trigger: Axis(x=0.0, y=0.0)
Controller right second trigger: Axis(x=0.0, y=0.0)
"""

import copy
import os
import time

import openvr

from vrchat_recorder.vr.tracking_recorder import TrackingRecorder

openvr.init(openvr.VRApplication_Background)
vrsystem = openvr.VRSystem()

tr = TrackingRecorder("demo.bin", vrsystem, frame_rate=60)
tr.record_background()


try:
    while True:
        holder = copy.deepcopy(tr._holder)
        text = f"""\
---
timestamp: {holder.timestamp}
HMD position: {holder.hmd.position}
HMD orientation: {holder.hmd.orientation}

Controller left position: {holder.controller.left.position}
Controller left orientation: {holder.controller.left.orientation}
Controller left thumb stick: {holder.controller.left.thumb_stick}
Controller left first trigger: {holder.controller.left.first_trigger}
Controller left second trigger: {holder.controller.left.second_trigger}

Controller right position: {holder.controller.right.position}
Controller right orientation: {holder.controller.right.orientation}
Controller right thumb stick: {holder.controller.right.thumb_stick}
Controller right first trigger: {holder.controller.right.first_trigger}
Controller right second trigger: {holder.controller.right.second_trigger}
"""
        os.system("cls" if os.name == "nt" else "clear")  # Clear console
        print(text, end="\r")
        time.sleep(0.001)
except KeyboardInterrupt:
    pass

tr.shutdown()

file_stats = os.stat("demo.bin")

print(f"File size: {file_stats.st_size} bytes")
