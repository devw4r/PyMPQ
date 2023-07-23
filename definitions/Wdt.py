from io import BytesIO

from definitions.Adt import Adt
from definitions.chunks.TileHeader import TileHeader
from definitions.reader.StreamReader import StreamReader
from definitions.utils.Constants import Constants


class Wdt:
    def __init__(self, dbc_map, mpq_reader):
        self.name = dbc_map.name
        self.mpq_reader = mpq_reader
        self.stream_reader = None
        self.dbc_map = dbc_map
        self.adt_version = 0  # 18
        self.tile_information = [[type[TileHeader] for _ in range(64)] for _ in range(64)]
        self.adt_data = [[type[Adt] for _ in range(64)] for _ in range(64)]

    def __enter__(self):
        mpq_entry = self.mpq_reader.mpq_entries[0]
        self.stream_reader = StreamReader(BytesIO(self.mpq_reader.read_file_bytes(mpq_entry)))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.stream_reader:
            self.stream_reader.close()
        self.stream_reader = None
        self.mpq_reader = None
        self.tile_information.clear()
        self.adt_data.clear()
        self.tile_information = None
        self.adt_data = None

    def process(self):
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

        # Move to next token.
        token, size = self.stream_reader.read_chunk_information(forward=size)
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

        # Move to next token.
        token, size = self.stream_reader.read_chunk_information(forward=size)
        if 'MONM' not in token:
            print(f'Invalid Token')
            return
        elif not size:
            print(f'Map [{self.dbc_map.name}] does not contain tile data, skipping.')
            return

        # Move to next token.
        token, size = self.stream_reader.read_chunk_information(forward=size)
        # Optional for WMO based.
        if 'MODF' in token:
            print(f'Map [{self.dbc_map.name}] is WMO based, skipping.')
            return

        if 'MHDR' not in token:
            print(f'Invalid Token')
            return

        # ADT data.
        total = Constants.TILE_BLOCK_SIZE * Constants.TILE_BLOCK_SIZE
        current = 0
        for x in range(Constants.TILE_BLOCK_SIZE):
            for y in range(Constants.TILE_BLOCK_SIZE):
                current += 1
                tile_info: TileHeader = self.tile_information[x][y]
                if tile_info and tile_info.size:
                    with Adt.from_reader(tile_info, x, y, self.stream_reader) as adt:
                        adt.process()
                self.progress(f'Processing ADT tiles for [{self.dbc_map.name}]...', current, total)

    def progress(self, msg, current, total):
        msg = f'{msg} [{current}/{total}] ({int(current * 100 / total)}%)'
        if current != total:
            print(f'[PROGRESS] {msg}', end='\r')
        else:
            print(f'[COMPLETE] {msg}')
