# An example that uses the RadSens CircuitPython library for use on a Raspberry Pi Pico W.
# https://julianmcconnell.com
# Version 20231129a

import board
import time
import busio
from RadSens import CG_RadSens

# Initialize I2C for the main program
i2c = busio.I2C(sda=board.GP20, scl=board.GP21)

# Create an instance of the CG_RadSens class and pass the i2c object
sensor = CG_RadSens(i2c)

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
