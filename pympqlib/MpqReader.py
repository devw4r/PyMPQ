from io import BytesIO
import zlib


class MpqReader:
    def __init__(self, mpq_archive, mpq_entry):
        self.mpq_archive = mpq_archive
        self.stream = mpq_archive.stream
        self.entry_stream = None
        self.mpq_entry = mpq_entry
        self.buffer_size = 0x40000
        self.block_size = mpq_archive.block_size
        self.current_block_index = -1
        self._position = 0
        self.data = b''
        self.length = mpq_entry.file_size
        self._fill()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.data = None
        self.entry_stream.close()

    def end_of_stream(self):
        if not self.data or not self.entry_stream:
            return True
        return self.entry_stream.tell() >= len(self.data)

    def read_line(self):
        if not self.data or not self.entry_stream:
            return 'Error'
        line_bytes = self.entry_stream.readline().strip()
        return line_bytes.decode('utf-8')

    def _fill(self):
        if self.mpq_entry.is_single_unit():
            return self._read_single_unit()

        to_read = self.buffer_size
        read_total = 0

        while to_read > 0:
            read = self._read_internal(to_read)
            if not read:
                break
            read_total += read
            to_read -= read

        self.entry_stream = BytesIO(self.data)

    def _read_internal(self, to_read):
        if self._position >= self.length:
            return 0

        block_bytes_count = self._buffer_data()
        if not block_bytes_count:
            return 0

        return block_bytes_count

    def _buffer_data(self):
        required_block = int(self._position / self.block_size)
        if required_block != self.current_block_index:
            expected_length = int(min(self.length - (required_block * self.block_size), self.block_size))
            block_data = self._load_block(required_block, expected_length)
            self.data += block_data
            self.current_block_index = required_block
            self._position = len(self.data)
            return len(block_data)
        return 0

    def _load_block(self, required_block, expected_length):
        if self.mpq_entry.is_compressed():
            offset = self.mpq_entry.block_positions[required_block]
            to_read = int(self.mpq_entry.block_positions[required_block + 1] - offset)
        else:
            offset = required_block * self.block_size
            to_read = expected_length

        offset += self.mpq_entry.file_pos

        self.stream.seek(offset)
        data = self.stream.read(to_read)
        if len(data) != to_read:
            return False

        if self.mpq_entry.is_encrypted():
            if not self.mpq_entry.encryption_seed:
                return False

            encryption_seed = required_block + self.mpq_entry.encryption_seed
            data = self.mpq_archive.decrypt_block_from_bytes(data, encryption_seed)

        if self.mpq_entry.is_compressed() and to_read != expected_length:
            if self.mpq_entry.is_compressed_multi():
                data = self._decompress_multi(data, expected_length)
            else:
                data = self._pk_decompress(data, expected_length)

        return data

    def _decompress_multi(self, data, expected_length):
        stream = BytesIO(data)
        comp_type = ord(stream.read(1))

        if comp_type == 1:  # Huffman:
            pass
        elif comp_type == 2:  # ZLib/Deflate
            return zlib.decompress(stream.read(), bufsize=expected_length)
        elif comp_type == 8:  # PKLib / Impode
            pass
        elif comp_type == 0x10:  # BZip2
            pass
        elif comp_type == 0x80:  # IMA ADPCM Stereo
            pass
        elif comp_type == 0x40:  # IMA ADPCM Mono
            pass
        elif comp_type == 0x12:  # LZMA
            pass
        elif comp_type == 0x22:  # Sparse then ZLib.
            pass
        elif comp_type == 0x30:  # Sparse then BZip2.
            pass
        elif comp_type == 0x41:  #  Huffman then Wav.
            pass
        elif comp_type == 0x48:  #  PKLib then Wav.
            pass

    def _read_single_unit(self):
        return
