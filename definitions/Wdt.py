from io import BytesIO

from definitions.Adt import Adt
from definitions.chunks.TileHeader import TileHeader
from definitions.reader.StreamReader import StreamReader
from definitions.utils.Constants import Constants


class Wdt:
    def __init__(self, dbc_map, mpq_reader):
        self.name = dbc_map.name_en_us
        self.stream_reader = StreamReader(BytesIO(mpq_reader.read_file_bytes(mpq_reader.mpq_entries[0])))
        self.dbc_map = dbc_map
        self.adt_version = 0  # 18
        self.tile_information = [[type[TileHeader] for _ in range(64)] for _ in range(64)]
        self.adt_data = [[type[Adt] for _ in range(64)] for _ in range(64)]

    def parse(self):
        token, size = self.stream_reader.read_chunk_information()
        if 'MVER' not in token:
            print('Invalid Token')
            return

        self.adt_version = self.stream_reader.read_int()
        if self.adt_version != 18:
            print('Wrong ADT version.')
            return

        token, size = self.stream_reader.read_chunk_information()
        if 'MPHD' not in token:
            print('Invalid Token')
            return

        # Discard.
        self.stream_reader.move_forward(size)

        token, size = self.stream_reader.read_chunk_information()
        if 'MAIN' not in token:
            print(f'Invalid Token')
            return

        # Tiles information.
        for x in range(64):
            for y in range(64):
                self.tile_information[x][y] = TileHeader.from_reader(self.stream_reader)

        token, size = self.stream_reader.read_chunk_information()
        if 'MDNM' not in token:
            print(f'Invalid Token')
            return

        # Discard.
        self.stream_reader.move_forward(size)

        token, size = self.stream_reader.read_chunk_information()
        if 'MONM' not in token:
            print(f'Invalid Token')
            return

        # Discard.
        self.stream_reader.move_forward(size)

        token, size = self.stream_reader.read_chunk_information()
        # Optional for WMO based.
        if 'MODF' in token:
            # Discard.
            self.stream_reader.move_forward(size)

        # ADT,
        if 'MHDR' not in token:
            print(f'Invalid Token')
            return

        for x in range(Constants.TILE_BLOCK_SIZE):
            for y in range(Constants.TILE_BLOCK_SIZE):
                tile_info: TileHeader = self.tile_information[x][y]
                if not tile_info or not tile_info.size:
                    continue
                self.adt_data[x][y] = Adt.from_reader(tile_info, x, y, self.stream_reader)

        print(len(self.adt_data))

