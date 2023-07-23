from definitions.chunks.TileHeader import TileHeader
from definitions.chunks.TileInformation import TileInformation
from definitions.utils.Constants import Constants


class Adt:
    def __init__(self, x, y):
        self.adt_x = x
        self.adt_y = y
        self.chunks_information = [[type[TileHeader] for _ in range(16)] for _ in range(16)]
        self.adt_tiles = [[type[TileInformation] for _ in range(16)] for _ in range(16)]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.chunks_information.clear()
        self.adt_tiles.clear()
        self.chunks_information = None
        self.adt_tiles = None

    def process(self):
        pass

    @staticmethod
    def from_reader(adt_x, adt_y, stream_reader):
        # Initialize adt object.
        adt = Adt(adt_x, adt_y)

        error, token, size = stream_reader.read_chunk_information('MHDR')
        if error:
            print(f'[WARNING] {error}')
            return

        # 16x16 chunk map.
        error, token, size = stream_reader.read_chunk_information('MCIN', skip=size)
        if error:
            print(f'[WARNING] {error}')
            return

        for x in range(Constants.TILE_SIZE):
            for y in range(Constants.TILE_SIZE):
                adt.chunks_information[x][y] = TileHeader.from_reader(stream_reader)

        error, token, size = stream_reader.read_chunk_information('MTEX')
        if error:
            print(f'[WARNING] {error}')
            return

        # Move to next token. (Optional)
        error, token, size = stream_reader.read_chunk_information('MDDF', skip=size)
        if error:
            print(f'[WARNING] {error}')
            return

        # Move to next token. (Optional)
        error, token, size = stream_reader.read_chunk_information('MODF', skip=size)
        if error:
            print(f'[WARNING] {error}')
            return

        # ADT data.
        for x in range(Constants.TILE_SIZE):
            for y in range(Constants.TILE_SIZE):
                stream_reader.set_position(adt.chunks_information[x][y].offset)
                error, token, size = stream_reader.read_chunk_information('MCNK')
                if error:
                    print(f'[WARNING] {error}')
                    return
                adt.adt_tiles[x][y] = TileInformation.from_reader(stream_reader)

        return adt
