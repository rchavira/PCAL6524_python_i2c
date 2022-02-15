from smbus2 import SMBus, i2c_msg

class I2Cdevice(object):
    __slots__ = ["address", "busIO"]
    def __init__(self, address, busIO):
        self.address = address
        self.busIO = busIO

    def write_msg(self, data):
        return i2c_msg.write(self.address, data)

    def read_msg(self, read_len):
        return i2c_msg.read(self.address, read_len)

    def read_write(self, write_data, read_len):
        write = self.write_msg(write_data)
        if read_len > 0:
            read = self.read_msg(read_len)
        else
            read = None

        with SMBus(self.busIO) as bus:
            if read_len > 0:
                bus.i2c_rdwr(write, read)
            else:
                bus.i2c_rdwr(write)

        if read is not None:
            return list(read)
        else:
            return None
