from definitions.chunks.TileHeader import TileHeader
from definitions.chunks.TileInformation import TileInformation
from definitions.utils.Constants import Constants


class Adt:
    def __init__(self, x, y):
        self.adt_x = x
        self.adt_y = y
        self.chunks_information = [[type[TileHeader] for _ in range(16)] for _ in range(16)]
        self.adt_tiles = [[type[TileInformation] for _ in range(16)] for _ in range(16)]

    @staticmethod
    def from_reader(tile_info: TileHeader, adt_x, adt_y, stream_reader):
        adt = Adt(adt_x, adt_y)

        stream_reader.set_position(tile_info.offset)

        token, size = stream_reader.read_chunk_information()
        # Area header.
        if 'MHDR' not in token:
            print(f'Invalid Token')
            return

        # Discard.
        stream_reader.move_forward(size)

        token, size = stream_reader.read_chunk_information()
        # 16x16 chunk map.
        if 'MCIN' not in token:
            print(f'Invalid Token')
            return

        for x in range(Constants.TILE_SIZE):
            for y in range(Constants.TILE_SIZE):
                adt.chunks_information[x][y] = TileHeader.from_reader(stream_reader)

        token, size = stream_reader.read_chunk_information()
        # 16x16 chunk map.
        if 'MTEX' not in token:
            print(f'Invalid Token')
            return

        # Discard.
        stream_reader.move_forward(size)

        token, size = stream_reader.read_chunk_information()
        # 16x16 chunk map.
        if 'MDDF' not in token:
            print(f'Invalid Token')
            return

        # Discard.
        stream_reader.move_forward(size)

        token, size = stream_reader.read_chunk_information()
        # 16x16 chunk map.
        if 'MODF' not in token:
            print(f'Invalid Token')
            return

        # Discard.
        stream_reader.move_forward(size)

        for x in range(Constants.TILE_SIZE):
            for y in range(Constants.TILE_SIZE):
                stream_reader.set_position(adt.chunks_information[x][y].offset)
                token, size = stream_reader.read_chunk_information()
                if 'MCNK' not in token:
                    print(f'Invalid Token')
                    return
                adt.adt_tiles[x][y] = TileInformation.from_reader(stream_reader)

        return adt
