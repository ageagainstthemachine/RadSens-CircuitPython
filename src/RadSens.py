# The CG_RadSens library converted to CircuitPython for use on a Raspberry Pi Pico W.
#
# Please see the original Arduino library here: https://github.com/climateguard/RadSens
# Please see the device here: https://climateguard.info/

# Import necessary CircuitPython libraries
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice

# Define constants for the RadSens device

# Default radSens i2c device address
RS_DEFAULT_I2C_ADDRESS = 0x66

# Register definitions
RS_DEVICE_ID_RG = 0x00
RS_FIRMWARE_VER_RG = 0x01
RS_RAD_INTENSY_DYNAMIC_RG = 0x03
RS_RAD_INTENSY_STATIC_RG = 0x06
RS_PULSE_COUNTER_RG = 0x09
RS_DEVICE_ADDRESS_RG = 0x10
RS_HV_GENERATOR_RG = 0x11
RS_SENSITIVITY_RG = 0x12
RS_LED_CONTROL_RG = 0x14
RS_LMP_MODE_RG = 0x0C

# RadSens class definition
class CG_RadSens:
    def __init__(self, sensor_address=RS_DEFAULT_I2C_ADDRESS):
        # Initialize I2C interface
        self.i2c = busio.I2C(sda=board.GP0, scl=board.GP1, frequency=100000)
        self._sensor_address = sensor_address
        self._chip_id = 0
        self._firmware_ver = 0
        self._pulse_cnt = 0

    def init(self):
        # Check if the sensor is connected
        device = I2CDevice(self.i2c, self._sensor_address)
        try:
            with device as i2c_bus:
                i2c_bus.write(bytes([0x0]))
        except OSError:
            return False

        # Get chip ID and firmware version
        self._chip_id, self._firmware_ver = self.i2c_read(RS_DEVICE_ID_RG, 2)
        return True

    def i2c_read(self, reg_addr, num_bytes):
        # Read data from I2C
        device = I2CDevice(self.i2c, self._sensor_address)
        buffer = bytearray(num_bytes)
        with device as i2c_bus:
            i2c_bus.write(bytes([reg_addr]))
            i2c_bus.readinto(buffer)
        return buffer

    def get_chip_id(self):
        """Get chip id, default value: 0x7D."""
        return self._chip_id

    def get_firmware_version(self):
        """Get firmware version."""
        return self._firmware_ver

    def get_rad_intensy_dynamic(self):
        """Get radiation intensity (dynamic period T < 123 sec)."""
        data = self.i2c_read(RS_RAD_INTENSY_DYNAMIC_RG, 3)
        return (data[0] << 16 | data[1] << 8 | data[2]) / 10.0

    def get_rad_intensy_static(self):
        """Get radiation intensity (static period T = 500 sec)."""
        data = self.i2c_read(RS_RAD_INTENSY_STATIC_RG, 3)
        return (data[0] << 16 | data[1] << 8 | data[2]) / 10.0

    def update_pulses(self):
        """Update the pulse count."""
        data = self.i2c_read(RS_PULSE_COUNTER_RG, 2)
        self._pulse_cnt += (data[0] << 8) | data[1]

    def get_number_of_pulses(self):
        """Get the accumulated number of pulses registered by the module since the last I2C data reading."""
        self.update_pulses()
        return self._pulse_cnt

    def get_sensor_address(self):
        """Get sensor address."""
        self._sensor_address = self.i2c_read(RS_DEVICE_ADDRESS_RG, 1)[0]
        return self._sensor_address

    def get_hv_generator_state(self):
        """Get state of high-voltage voltage Converter."""
        return self.i2c_read(RS_HV_GENERATOR_RG, 1)[0] == 1

    def get_sensitivity(self):
        """Get the value coefficient used for calculating the radiation intensity."""
        data = self.i2c_read(RS_SENSITIVITY_RG, 2)
        return data[1] * 256 + data[0]

    def set_hv_generator_state(self, state):
        """Control register for a high-voltage voltage Converter."""
        value = 1 if state else 0
        self.i2c.writeto(self._sensor_address, bytes([RS_HV_GENERATOR_RG, value]))

    def set_lp_mode(self, state):
        """Control register for a low power mode."""
        value = 1 if state else 0
        self.i2c.writeto(self._sensor_address, bytes([RS_LMP_MODE_RG, value]))

    def set_sensitivity(self, sens):
        """Set the sensitivity coefficient."""
        data = [(sens & 0xFF), (sens >> 8)]
        self.i2c.writeto(self._sensor_address, bytes([RS_SENSITIVITY_RG] + data))

    def set_led_state(self, state):
        """Control register for an indication diode."""
        value = 1 if state else 0
        self.i2c.writeto(self._sensor_address, bytes([RS_LED_CONTROL_RG, value]))

    def get_led_state(self):
        """Get state of led indication."""
        return self.i2c_read(RS_LED_CONTROL_RG, 1)[0] == 1
