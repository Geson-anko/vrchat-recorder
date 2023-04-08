"""This demonstrates how to use the ControllerEventRecorder class. Afts start recording in background, you can see the
controller events in output file.

You can also use `record_background` method to record in background thread.
"""
import openvr

from vrchat_recorder.vr.controller_event_recorder import ControllerEventRecorder

openvr.init(openvr.VRApplication_Background)
vrsystem = openvr.VRSystem()

cer = ControllerEventRecorder("controller_event_recorder_demo.csv", vrsystem)

print("Press Ctrl+C to stop recording.")
cer.record()
