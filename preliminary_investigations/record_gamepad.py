import csv
import time

import inputs

# Get the gamepad device
gamepad = inputs.devices.gamepads[0]

# Get the initial state
state = {}
for event in gamepad:
    state[event.ev_type + "_" + event.ev_name] = event.ev_value
    if len(state) == len(gamepad.capabilities()):
        break

# Initialize the CSV file
filename = "gamepad_data.csv"
with open(filename, "w", newline="") as csvfile:
    fieldnames = ["time"] + list(state.keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# Continuously record gamepad data to the CSV file
prev_state = None
while True:
    try:
        events = gamepad.read()
        current_time = time.time()
        current_state = dict(state)

        for event in events:
            current_state[event.ev_type + "_" + event.ev_name] = event.ev_value

        if current_state != prev_state:
            with open(filename, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                row = {"time": current_time}
                row.update(current_state)
                writer.writerow(row)
            prev_state = current_state
    except inputs.UnpluggedError:
        print("Gamepad disconnected.")
        break
