from struct import unpack


class StreamReader:
    def __init__(self, stream):
        self.stream = stream

    def close(self):
        if self.stream:
            self.stream.close()
        self.stream = None

    def read_chunk_information(self, forward=0, seek=0):
        if seek:
            self.set_position(seek)
        if forward:
            self.move_forward(forward)
        token = self.read_bytes(4)
        token_name = token.decode('utf8')[::-1]
        size = self.read_int()
        return token_name, size

    def set_position(self, position):
        self.stream.seek(position)

    def get_position(self):
        return self.stream.tell()

    def move_forward(self, length):
        self.stream.seek(self.get_position() + length)

    def read_bytes(self, length):
        return self.stream.read(length)

    def read_uint16(self):
        return unpack('<H', self.stream.read(2))[0]

    def read_int(self):
        return unpack('<I', self.stream.read(4))[0]

    def read_float(self):
        return unpack('<f', self.stream.read(4))[0]
