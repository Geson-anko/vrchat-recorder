import inputs
from inputs import get_gamepad

dev = inputs.devices.gamepads[0]
print(dev.name)

print_event_names = {"Absolute", "Key"}

i_prev_ABS_X = 0
i_prev_ABS_RX = 0
i_prev_ABS_Y = 0
i_prev_ABS_RY = 0
allow_diff = 1024

while True:
    events = get_gamepad()
    for event in events:
        ev_type: str = event.ev_type
        ev_code: str = event.code
        ev_state: int = event.state
        ts: float = event.timestamp

        if ev_type in print_event_names:
            if ev_type == "Absolute" and not ev_code.startswith("ABS_HAT"):
                if ev_code.endswith("X") or ev_code.endswith("Y"):
                    # if ev_code.endswith("_X"):
                    #     if abs(i_prev_ABS_X - ev_state) < allow_diff:
                    #         continue
                    #     else:
                    #         i_prev_ABS_X = ev_state

                    # if ev_code.endswith("_Y"):
                    #     if abs(i_prev_ABS_Y - ev_state) < allow_diff:
                    #         continue
                    #     else:
                    #         i_prev_ABS_Y = ev_state

                    ev_state = ev_state / 32768  # 2**15
                if ev_code.endswith("Z"):
                    ev_state = ev_state / 256

            s = f"{ts:.2f} {ev_type} {ev_code} {ev_state}"
            print(s)
