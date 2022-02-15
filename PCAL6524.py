# Commands
PCAL6524_INPUT_PORT_0 = 0x00
PCAL6524_INPUT_PORT_1 = 0x01
PCAL6524_INPUT_PORT_2 = 0x02

PCAL6524_OUTPUT_PORT_0 = 0x04
PCAL6524_OUTPUT_PORT_1 = 0x05
PCAL6524_OUTPUT_PORT_2 = 0x06

PCAL6524_POLARITY_INVERSION_PORT_0 = 0x08
PCAL6524_POLARITY_INVERSION_PORT_1 = 0x09
PCAL6524_POLARITY_INVERSION_PORT_2 = 0x0A

PCAL6524_CONFIGURATION_PORT_0 = 0x0C
PCAL6524_CONFIGURATION_PORT_1 = 0x0D
PCAL6524_CONFIGURATION_PORT_2 = 0x0E

PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_0A = 0x40
PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_0B = 0x41
PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_1A = 0x42
PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_1B = 0x43
PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_2A = 0x44
PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_2B = 0x45

PCAL6524_INPUT_LATCH_PORT_0 = 0x48
PCAL6524_INPUT_LATCH_PORT_1 = 0x49
PCAL6524_INPUT_LATCH_PORT_2 = 0x4A

PCAL6524_PULL_UP_PULL_DOWN_ENABLE_PORT_0 = 0x4C
PCAL6524_PULL_UP_PULL_DOWN_ENABLE_PORT_1 = 0x4D
PCAL6524_PULL_UP_PULL_DOWN_ENABLE_PORT_2 = 0x4E

PCAL6524_PULL_UP_PULL_DOWN_SELECTION_PORT_0 = 0x50
PCAL6524_PULL_UP_PULL_DOWN_SELECTION_PORT_1 = 0x51
PCAL6524_PULL_UP_PULL_DOWN_SELECTION_PORT_2 = 0x52

PCAL6524_INTERRUPT_MASK_PORT_0 = 0x54
PCAL6524_INTERRUPT_MASK_PORT_1 = 0x55
PCAL6524_INTERRUPT_MASK_PORT_2 = 0x56

PCAL6524_INTERRUPT_STATUS_PORT_0 = 0x58
PCAL6524_INTERRUPT_STATUS_PORT_1 = 0x59
PCAL6524_INTERRUPT_STATUS_PORT_2 = 0x5A

PCAL6524_OUTPUT_CONFIGURATION = 0x5C

PCAL6524_INTERRUPT_EDGE_PORT_0A = 0x60
PCAL6524_INTERRUPT_EDGE_PORT_0B = 0x61
PCAL6524_INTERRUPT_EDGE_PORT_1A = 0x62
PCAL6524_INTERRUPT_EDGE_PORT_1B = 0x63
PCAL6524_INTERRUPT_EDGE_PORT_2A = 0x64
PCAL6524_INTERRUPT_EDGE_PORT_2B = 0x65

PCAL6524_INTERRUPT_CLEAR_PORT_0 = 0x68
PCAL6524_INTERRUPT_CLEAR_PORT_1 = 0x69
PCAL6524_INTERRUPT_CLEAR_PORT_2 = 0x6A

PCAL6524_INPUT_STATUS_PORT_0 = 0x6C
PCAL6524_INPUT_STATUS_PORT_1 = 0x6D
PCAL6524_INPUT_STATUS_PORT_2 = 0x6E

PCAL6524_INDIVIDUAL_PIN_OUTPUT_PORT_0 = 0x70
PCAL6524_INDIVIDUAL_PIN_OUTPUT_PORT_1 = 0x71
PCAL6524_INDIVIDUAL_PIN_OUTPUT_PORT_2 = 0x72

PCAL6524_SWITCH_DEBOUNCE_ENABLE_0 = 0x74
PCAL6524_SWITCH_DEBOUNCE_ENABLE_1 = 0x75
PCAL6524_SWITCH_DEBOUNCE_COUNT = 0x76

from i2c_device import I2Cdevice
from smbus2 import SMBus, i2c_msg
import time

class PCAL6524_Device(I2Cdevice):
    def __init__(self, address, busIO, **kwargs):
        super().__init__(address, busIO)
        self.input_registers = {}
        self.output_registers = {}
        self.polarity_registers = {}
        self.configuration_registers = {}
        self.input_latch_registers = {}
        self.pull_up_pull_down_registers = {}
        self.interrupt_mask_registers = {}
        self.interrupt_status_registers = {}
        self.output_drive_strength_registers = {}
        self.interrupt_clear_register = {}
        self.output_configuration = 0

    def read_msg(self, read_len):
        return i2c_msg.read(self.address | 0x01, read_len)

    def read_inputs(self):
        data = [PCAL6524_INPUT_PORT_0]
        result = self.read_write(data, 3)
        for i in range(3):
            self.input_registers[i] = result[i]

    def read_outputs(self):
        data = [PCAL6524_OUTPUT_PORT_0]
        self.output_registers = self.read_write(data, 3)
        result = self.read_write(data, 3)
        for i in range(3):
            self.output_registers[i] = result[i]

    def write_output_port(self, port, data):
        cmd = [PCAL6524_OUTPUT_PORT_0,PCAL6524_OUTPUT_PORT_1,PCAL6524_OUTPUT_PORT_2]
        data = [cmd[port], data]
        self.read_write(data, 0)

    def write_outputs(self, port0, port1, port2)
        data = [PCAL6524_OUTPUT_PORT_0, port0, port1, port2]
        self.read_write(data, 0)

    def read_polarity(self):
        data = [PCAL6524_POLARITY_INVERSION_PORT_0]
        result = self.read_write(data, 3)
        for i in range(3):
            self.polarity_registers[i] = result[i]

    def write_polarity(self, port0, port1, port2):
        data = [PCAL6524_POLARITY_INVERSION_PORT_0, port0, port1, port2]
        self.read_write(data, 0)

    def read_configurations(self):
        data = [PCAL6524_CONFIGURATION_PORT_0]
        result = self.read_write(data, 3)
        for i in range(3):
            self.configuration_registers[i] = result[i]

    def write_configurations(self, port0, port1, port2):
        data = [PCAL6524_CONFIGURATION_PORT_0, port0, port1, port2]
        self.read_write(data, 0)

    def read_output_drive_strength(self, port):
        p1 = [PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_0A, PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_1A, PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_2A]
        p2 = [PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_0B, PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_1B, PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_2B]

        data1 = self.read_write([p1[port]], 1)
        data2 = self.read_write([p1[port]], 1)

        self.output_drive_strength_registers[port] = data2.extend(data1)

    def write_output_drive_strength(self, port, dataA, dataB):
        p1 = [PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_0A, PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_1A, PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_2A]
        p2 = [PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_0B, PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_1B, PCAL6524_OUTPUT_DRIVE_STRENGTH_PORT_2B]

        data1 = [p1[port], dataA]
        data2 = [p2[port], dataB]

        self.read_write(data1, 0)
        self.read_write(data2, 0)

    def read_input_latch_register(self, port):
        p = [PCAL6524_INPUT_LATCH_PORT_0, PCAL6524_INPUT_LATCH_PORT_1, PCAL6524_INPUT_LATCH_PORT_2]
        result = self.read_write([p[port]], 1)
        self.input_latch_registers[port] = result[0]

    def write_input_latch(self, port, data)
        p = [PCAL6524_INPUT_LATCH_PORT_0, PCAL6524_INPUT_LATCH_PORT_1, PCAL6524_INPUT_LATCH_PORT_2]
        self.read_write([p[port], data], 0)

    def read_pull_enable_registers(self, port):
        p = [PCAL6524_PULL_UP_PULL_DOWN_ENABLE_PORT_0, PCAL6524_PULL_UP_PULL_DOWN_ENABLE_PORT_1, PCAL6524_PULL_UP_PULL_DOWN_ENABLE_PORT_2]
        result = self.read_write([p[port]], 1)
        self.read_pull_enable_registers[port] = result[0]

    def write_pull_enable_registers(self, port, data):
        p = [PCAL6524_PULL_UP_PULL_DOWN_ENABLE_PORT_0, PCAL6524_PULL_UP_PULL_DOWN_ENABLE_PORT_1, PCAL6524_PULL_UP_PULL_DOWN_ENABLE_PORT_2]
        result = self.read_write([p[port], data], 0)

    def read_pull_registers(self, port):
        p = [PCAL6524_PULL_UP_PULL_DOWN_SELECTION_PORT_0, PCAL6524_PULL_UP_PULL_DOWN_SELECTION_PORT_1, PCAL6524_PULL_UP_PULL_DOWN_SELECTION_PORT_2]
        result = self.read_write([p[port]], 1)
        self.pull_up_pull_down_registers[port] = result[0]

    def write_pull_registers(self, port, data):
        p = [PCAL6524_PULL_UP_PULL_DOWN_SELECTION_PORT_0, PCAL6524_PULL_UP_PULL_DOWN_SELECTION_PORT_1, PCAL6524_PULL_UP_PULL_DOWN_SELECTION_PORT_2]
        result = self.read_write([p[port], data], 0)

    def read_interrupt_mask(self, port):
        p = [PCAL6524_INTERRUPT_MASK_PORT_0, PCAL6524_INTERRUPT_MASK_PORT_1, PCAL6524_INTERRUPT_MASK_PORT_2]
        result = self.read_write([p[port]], 1)
        self.interrupt_mask_registers[port] = result[0]

    def write_interrupt_mask(self, port, data):
        p = [PCAL6524_INTERRUPT_MASK_PORT_0, PCAL6524_INTERRUPT_MASK_PORT_1, PCAL6524_INTERRUPT_MASK_PORT_2]
        result = self.read_write([p[port], data], 0)

    def read_interrupt_status(self, port):
        p = [PCAL6524_INTERRUPT_MASK_PORT_0, PCAL6524_INTERRUPT_MASK_PORT_1, PCAL6524_INTERRUPT_MASK_PORT_2]
        result = self.read_write([p[port]], 1)
        self.interrupt_status_registers[port] = result[0]

    def write_interrupt_mask(self, port, data):
        p = [PCAL6524_INTERRUPT_MASK_PORT_0, PCAL6524_INTERRUPT_MASK_PORT_1, PCAL6524_INTERRUPT_MASK_PORT_2]
        result = self.read_write([p[port], data], 0)

    def read_output_configuration(self):
        p = [PCAL6524_OUTPUT_CONFIGURATION]
        result =self.read_write(p, 1)
        self.output_configuration = result[0]

    def write_output_configuration(self, data):
        p = [PCAL6524_OUTPUT_CONFIGURATION, data]
        result =self.read_write(p, 0)

    def read_interrupt_clear(self, port):
        p = [PCAL6524_INTERRUPT_CLEAR_PORT_0, PCAL6524_INTERRUPT_CLEAR_PORT_1, PCAL6524_INTERRUPT_CLEAR_PORT_2]
        result = self.read_write([p[port]], 1)
        self.interrupt_clear_register[port] = result[0]

    def write_interrupt_clear(self, port, data):
        p = [PCAL6524_INTERRUPT_CLEAR_PORT_0, PCAL6524_INTERRUPT_CLEAR_PORT_1, PCAL6524_INTERRUPT_CLEAR_PORT_2]
        result = self.read_write([p[port], data], 0)

    def read_input_status(self, port):
        p = [PCAL6524_INPUT_STATUS_PORT_0, PCAL6524_INPUT_STATUS_PORT_1, PCAL6524_INPUT_STATUS_PORT_2]
        result = self.read_write([p[port]], 1)
        self.interrupt_clear_register[port] = result[0]
