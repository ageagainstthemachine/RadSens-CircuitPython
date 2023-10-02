# An example that uses the RadSens CircuitPython library for use on a Raspberry Pi Pico W.
# https://julianmcconnell.com
# Version 20231001a

import board
import time
from RadSens import CG_RadSens

# Initialize the RadSens sensor with the default I2C address
sensor = CG_RadSens()

# Initialize the sensor
if sensor.init():
    print("CG_RadSens initialized successfully!")
else:
    print("Failed to initialize CG_RadSens!")
    while True:
        pass  # Halt execution

while True:
    # Print chip ID and firmware version
    print("Chip ID:", sensor.get_chip_id())
    print("Firmware Version:", sensor.get_firmware_version())

    # Print radiation intensity (dynamic and static)
    print("Radiation Intensity (Dynamic):", sensor.get_rad_intensy_dynamic(), "uR/h")
    print("Radiation Intensity (Static):", sensor.get_rad_intensy_static(), "uR/h")

    # Print the accumulated number of pulses
    print("Number of Pulses:", sensor.get_number_of_pulses())

    # Print the sensor address
    print("Sensor Address:", hex(sensor.get_sensor_address()))

    # Print the state of the high-voltage voltage converter
    print("HV Generator State:", "ON" if sensor.get_hv_generator_state() else "OFF")

    # Print the sensitivity coefficient
    print("Sensitivity:", sensor.get_sensitivity(), "Imp/uR")

    # Print the state of the LED indication
    print("LED State:", "ON" if sensor.get_led_state() else "OFF")

    # Wait for 5 seconds before the next reading
    time.sleep(5)
