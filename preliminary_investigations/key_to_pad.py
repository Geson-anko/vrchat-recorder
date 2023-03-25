import keyboard
import pyvjoy
import time

# Set up the virtual controller
vjoy_device = pyvjoy.VJoyDevice(1)

# Main loop
running = True
while running:
    # Map W, A, S, D keys to controller stick input
    x, y = 0, 0
    if keyboard.is_pressed('w'):
        y = -1
    if keyboard.is_pressed('s'):
        y = 1
    if keyboard.is_pressed('a'):
        x = -1
    if keyboard.is_pressed('d'):
        x = 1

    # Normalize the stick input
    magnitude = (x ** 2 + y ** 2) ** 0.5
    if magnitude > 1:
        x /= magnitude
        y /= magnitude

    # Scale the stick input to the virtual controller's range
    x = int((x * 0.5 + 0.5) * 32767)
    y = int((y * 0.5 + 0.5) * 32767)

    # Send the stick input to the virtual controller
    vjoy_device.set_axis(pyvjoy.HID_USAGE_X, x)
    vjoy_device.set_axis(pyvjoy.HID_USAGE_Y, y)

    # Check for a specific key (e.g., 'q') to exit the loop
    if keyboard.is_pressed('q'):
        running = False

    time.sleep(0.001)