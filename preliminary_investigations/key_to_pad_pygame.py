import time

import pygame
import pyvjoy

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Keyboard to Controller Stick Emulation")

# Set up the virtual controller
vjoy_device = pyvjoy.VJoyDevice(1)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current state of the keyboard
    keys = pygame.key.get_pressed()

    # Map W, A, S, D keys to controller stick input
    x, y = 0, 0
    if keys[pygame.K_w]:
        y = -1
    if keys[pygame.K_f]:
        y = 1
    if keys[pygame.K_a]:
        x = -1
    if keys[pygame.K_d]:
        x = 1

    # Normalize the stick input
    magnitude = (x**2 + y**2) ** 0.5
    if magnitude > 1:
        x /= magnitude
        y /= magnitude

    # Scale the stick input to the virtual controller's range
    x = int((x * 0.5 + 0.5) * 32767)
    y = int((y * 0.5 + 0.5) * 32767)

    # Send the stick input to the virtual controller
    vjoy_device.set_axis(pyvjoy.HID_USAGE_X, x)
    vjoy_device.set_axis(pyvjoy.HID_USAGE_Y, y)

    # Refresh the display
    screen.fill((0, 0, 0))
    pygame.display.flip()
    time.sleep(0.005)

# Clean up
pygame.quit()
