"""
USB Volume Control using Rotary Encoder as HID Consumer Control Device
How to install libraries and setup Pico:
    https://www.onetransistor.eu/2021/04/media-keys-rpi-pico-circuitpython.html?sc=1721363204924#c4698244853129018643

This code uses a rotary encoder to control the volume of the computer.
The rotary encoder is connected to the Raspberry Pi Pico and acts as a USB HID Consumer Control device.
The code uses the adafruit_hid library to send volume up and volume down commands to the computer.
One more modification that can be added is a push button to mute/unmute the volume (not implemented in this code).

Modified by: Temirlan504
"""

import board
import digitalio
import time

import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Define the pins for the rotary encoder
encoder_pin_a = digitalio.DigitalInOut(board.GP1)
encoder_pin_b = digitalio.DigitalInOut(board.GP3)

# Set the pins as inputs with pull-up resistors
encoder_pin_a.direction = digitalio.Direction.INPUT
encoder_pin_b.direction = digitalio.Direction.INPUT
encoder_pin_a.pull = digitalio.Pull.UP
encoder_pin_b.pull = digitalio.Pull.UP

# Initialize variables to keep track of the encoder state
last_state_a = encoder_pin_a.value
last_state_b = encoder_pin_b.value

# Initialize USB device
consumer = ConsumerControl(usb_hid.devices)

debounce_delay = 0.01

while True:
    # Read the current state of the encoder pins
    current_state_a = encoder_pin_a.value
    current_state_b = encoder_pin_b.value

    # Check if the state of pin A has changed
    if current_state_a != last_state_a:
        # Check the state of pin B to determine rotation direction
        if current_state_a != current_state_b:
            consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
        else:
            consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
        
        # Debouncing delay
        time.sleep(debounce_delay)

    # Update the last state of the encoder pins
    last_state_a = current_state_a
    last_state_b = current_state_b
