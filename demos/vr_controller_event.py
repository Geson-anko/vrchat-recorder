"""This demonstrates how to use the ControllerEventRecorder class. Afts start recording in background, you can see the
controller events in output file.

You can also use `record_background` method to record in background thread.
"""
from pathlib import Path

import openvr

from vrchat_recorder.vr.controller_event_recorder import ControllerEventRecorder

openvr.init(openvr.VRApplication_Background)
vrsystem = openvr.VRSystem()


output_file_path = Path(__file__).parent / "output" / "controller_event_recorder_demo.csv"

cer = ControllerEventRecorder(output_file_path, vrsystem)

print("Press Ctrl+C to stop recording.")
cer.record()
