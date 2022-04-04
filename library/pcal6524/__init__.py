from i2cdevice import Device, Register, BitField, _int_to_bytes
from i2cdevice.adapter import LookupAdapter, Adapter
import struct

__version__ = '0.0.1'

I2C_ADDRESSES = [0x40, 0x42, 0x44, 0x46]
I2C_ADDRESS_DEFAULT = 0x67

CHIP_ID = 0x106

port_fields = (
    BitField('b0', 0b00000001),
    BitField('b1', 0b00000010),
    BitField('b2', 0b00000100),
    BitField('b3', 0b00001000),
    BitField('b4', 0b00010000),
    BitField('b5', 0b00100000),
    BitField('b6', 0b01000000),
    BitField('b7', 0b10000000)
)

twobit_fields = (
    BitField('b0', 0b00000011),
    BitField('b1', 0b00001100),
    BitField('b2', 0b00110000),
    BitField('b3', 0b11000000)
)


registers = (
    Register("RESET", 0x00, fields=(
       BitField('reset', 0xff, bit_width=8)
    )),
    Register("DEVICE_ID", 0xF0, fields=(
        BitField('manufacturer', 0b111111111111000000000000, bit_width=12),
        BitField('id', 0b000000000000111111111000, bit_width=9),
        BitField('revision', 0b000000000000000000000111, bit_width=3))),
    Register("INPUT_PORT_0", 0x00, fields=port_fields),
    Register("INPUT_PORT_1", 0x01, fields=port_fields),
    Register("INPUT_PORT_2", 0x02, fields=port_fields),
    Register("OUTPUT_PORT_0", 0x04, fields=port_fields),
    Register("OUTPUT_PORT_1", 0x05, fields=port_fields),
    Register("OUTPUT_PORT_2", 0x06, fields=port_fields),
    Register("POLARITY_INVERSION_PORT_0", 0x08, fields=port_fields),
    Register("POLARITY_INVERSION_PORT_1", 0x09, fields=port_fields),
    Register("POLARITY_INVERSION_PORT_2", 0x0A, fields=port_fields),
    Register("CONFIGURATION_PORT_0", 0x0C, fields=port_fields),
    Register("CONFIGURATION_PORT_1", 0x0D, fields=port_fields),
    Register("CONFIGURATION_PORT_2", 0x0E, fields=port_fields),
    Register("OUTPUT_DRIVE_STRENGTH_PORT_0A", 0x40, fields=twobit_fields),
    Register("OUTPUT_DRIVE_STRENGTH_PORT_0B", 0x41, fields=twobit_fields),
    Register("OUTPUT_DRIVE_STRENGTH_PORT_1A", 0x42, fields=twobit_fields),
    Register("OUTPUT_DRIVE_STRENGTH_PORT_1B", 0x43, fields=twobit_fields),
    Register("OUTPUT_DRIVE_STRENGTH_PORT_2A", 0x44, fields=twobit_fields),
    Register("OUTPUT_DRIVE_STRENGTH_PORT_2B", 0x45, fields=twobit_fields),
    Register("INPUT_LATCH_PORT_0", 0x48, fields=port_fields),
    Register("INPUT_LATCH_PORT_1", 0x49, fields=port_fields),
    Register("INPUT_LATCH_PORT_2", 0x4A, fields=port_fields),
    Register("PULL_UP_DOWN_ENABLE_PORT_0", 0x4C, fields=port_fields),
    Register("PULL_UP_DOWN_ENABLE_PORT_1", 0x4D, fields=port_fields),
    Register("PULL_UP_DOWN_ENABLE_PORT_2", 0x4E, fields=port_fields),
    Register("PULL_UP_DOWN_SELECTION_PORT_0", 0x50, fields=port_fields),
    Register("PULL_UP_DOWN_SELECTION_PORT_1", 0x51, fields=port_fields),
    Register("PULL_UP_DOWN_SELECTION_PORT_2", 0x52, fields=port_fields),
    Register("INTERRUPT_PORT_0", 0x54, fields=port_fields),
    Register("INTERRUPT_PORT_1", 0x55, fields=port_fields),
    Register("INTERRUPT_PORT_2", 0x56, fields=port_fields),
    Register("INTERRUPT_STATUS_PORT_0", 0x58, fields=port_fields),
    Register("INTERRUPT_STATUS_PORT_1", 0x59, fields=port_fields),
    Register("INTERRUPT_STATUS_PORT_2", 0x5A, fields=port_fields),
    Register("OUTPUT_CONFIGURATION", 0x5C, fields=(
        BitField('ODEN2', 0b00000100),
        BitField('ODEN1', 0b00000010),
        BitField('ODEN0', 0b00000001)
    )),
    Register("INTERRUPT_EDGE_PORT_0A", 0x60, fields=twobit_fields),
    Register("INTERRUPT_EDGE_PORT_0B", 0x61, fields=twobit_fields),
    Register("INTERRUPT_EDGE_PORT_1A", 0x62, fields=twobit_fields),
    Register("INTERRUPT_EDGE_PORT_1B", 0x63, fields=twobit_fields),
    Register("INTERRUPT_EDGE_PORT_2A", 0x64, fields=twobit_fields),
    Register("INTERRUPT_EDGE_PORT_2B", 0x65, fields=twobit_fields),
    Register("INTERRUPT_CLEAR_PORT_0", 0x68, fields=port_fields),
    Register("INTERRUPT_CLEAR_PORT_1", 0x69, fields=port_fields),
    Register("INTERRUPT_CLEAR_PORT_2", 0x6A, fields=port_fields),
    Register("INPUT_STATUS_PORT_0", 0x6C, fields=port_fields),
    Register("INPUT_STATUS_PORT_1", 0x6D, fields=port_fields),
    Register("INPUT_STATUS_PORT_2", 0x6E, fields=port_fields),
    Register("INDIVIDUAL_PIN_OUTPUT_PORT_0", 0x70, fields=port_fields),
    Register("INDIVIDUAL_PIN_OUTPUT_PORT_1", 0x71, fields=port_fields),
    Register("INDIVIDUAL_PIN_OUTPUT_PORT_2", 0x72, fields=port_fields),
    Register("SWITCH_DEBOUNCE_ENABLE_0", 0x74, fields=port_fields),
    Register("SWITCH_DEBOUNCE_ENABLE_1", 0x75, fields=port_fields),
    Register("SWITCH_DEBOUNCE_ENABLE_2", 0x76, fields=port_fields)
)


class PCAL6524:
    def __init__(self, i2c_addr, i2c_dev=None):
        self._i2c_addr = i2c_addr
        self._i2c_dev = i2c_dev
        self._pcal6524 = Device(
            I2C_ADDRESSES,
            i2c_dev=self._i2c_dev,
            bit_width=8,
            registers=registers
        )
        self._pcal6524.select_address(self._i2c_addr)

        try:
            chip = self._pcal6524.get('DEVICE_ID')
            if chip.id != CHIP_ID:
                raise RuntimeError("Unable to find pcal6524 on 0x{:02x}, CHIP_ID returned {:02x}".format(self._i2c_addr, chip.id))
        except IOError:
            raise RuntimeError("Unable to find pcal6524 on 0x{:02x}, IOError".format(self._i2c_addr))

    def _get_bit_list(self, register):
        prop_list = []
        for i in range(8):
            prop_list.append(self._get_prop(register, f'b{i}'))
        return prop_list

    def _get_prop(self, register, prop):
        return getattr(self._pcal6524.get(register), prop)

    def _set_bit_list(self, register, bits):
        kwargs = {}
        for i in range(8):
            kwargs[f'b{i}'] = bits[i]
        self._pcal6524.set(register, **kwargs)

    def _set_prop(self, register, prop, value):
        kwarg = {prop: value}
        self._pcal6524.set(register, **kwarg)

    def read_inputs(self, port):
        bits = self._get_bit_list(f'INPUT_PORT_{port}')
        return bits

    def read_outputs(self, port):
        bits = self._get_bit_list(f'OUTPUT_PORT_{port}')
        return bits

    def read_input_pin(self, port, pin):
        return self._get_prop(f'INPUT_PORT_{port}', f'b{pin}')

    def write_outputs(self, port, bits):
        self._set_bit_list(f"OUTPUT_PORT_{port}", bits)

    def write_output_pin(self, port, bit, bit_value):
        self._set_prop(f"OUTPUT_PORT_{port}", f"b{bit}", bit_value)

    def read_configuration(self, port):
        return self._get_bit_list(f"CONFIGURATION_PORT_{port}")

    def write_configuration(self, port, bits):
        self._set_bit_list(f"CONFIGURATION_PORT_{port}", bits)

    def read_polarity(self, port):
        return self._get_bit_list(f"POLARITY_INVERSION_PORT_{port}")

    def write_polarity(self, port, bits):
        self._set_bit_list(f"POLARITY_INVERSION_PORT_{port}", bits)

    def read_input_latch(self, port):
        return self._get_bit_list(f"INPUT_LATCH_PORT_{port}")

    def write_input_latch(self, port, bits):
        self._set_bit_list(f"INPUT_LATCH_PORT_{port}", bits)

    def read_pull_up_down_enable(self, port):
        return self._get_bit_list(f"PULL_UP_DOWN_ENABLE_PORT_{port}")

    def write_pull_up_down_enable(self, port, bits):
        self._set_bit_list(f"PULL_UP_DOWN_ENABLE_PORT_{port}", bits)

    def read_pull_up_down_selection(self, port):
        return self._get_bit_list(f"PULL_UP_DOWN_SELECTION_PORT_{port}")

    def write_pull_up_down_selection(self, port, bits):
        self._set_bit_list(f"PULL_UP_DOWN_SELECTION_PORT_{port}", bits)

    def read_interrupt(self, port):
        return self._get_bit_list(f"INTERRUPT_PORT_{port}")

    def write_interrupt(self, port, bits):
        self._set_bit_list(f"INTERRUPT_PORT_{port}", bits)

    def read_interrupt_status(self, port):
        return self._get_bit_list(f"INTERRUPT_STATUS_PORT_{port}")

    def write_interrupt_status(self, port, bits):
        self._set_bit_list(f"INTERRUPT_STATUS_PORT_{port}", bits)

    def read_interrupt_clear(self, port):
        return self._get_bit_list(f"INTERRUPT_CLEAR_PORT_{port}")

    def write_interrupt_clear(self, port, bits):
        self._set_bit_list(f"INTERRUPT_CLEAR_PORT_{port}", bits)

    def read_individual_pin_output(self, port):
        return self._get_bit_list(f"INDIVIDUAL_PIN_OUTPUT_PORT_{port}")

    def write_individual_pin_output(self, port, bits):
        self._set_bit_list(f"INDIVIDUAL_PIN_OUTPUT_PORT_{port}", bits)

    def read_switch_debounce_enable(self, port):
        return self._get_bit_list(f"SWITCH_DEBOUNCE_ENABLE_{port}")

    def write_switch_debounce_enable(self, port, bits):
        self._set_bit_list(f"SWITCH_DEBOUNCE_ENABLE_{port}", bits)
