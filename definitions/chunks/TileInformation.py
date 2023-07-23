from dataclasses import dataclass
from definitions.chunks.MCVT import MCVT


@dataclass
class TileInformation:
    flags: int
    has_liquids: bool
    area_number: int
    holes_low_mask: int
    offs_liquids: int
    mcvt: MCVT

    @staticmethod
    def from_reader(stream_reader):
        flags = stream_reader.read_int()
        has_liquids = flags & (0x4 | 0x8 | 0x10)
        offs_height = stream_reader.read_int(skip=20)
        area_number = stream_reader.read_int(skip=28)
        holes_low_mask = stream_reader.read_uint16(skip=4)
        offs_liquids = stream_reader.read_int(skip=34)
        header_offset = stream_reader.get_position(skip=24)

        # Read MCVT.
        stream_reader.set_position(offs_height + header_offset)
        mcvt = MCVT.from_reader(stream_reader)

        if offs_liquids and has_liquids:
            pass

        return TileInformation(flags, has_liquids, area_number, holes_low_mask, offs_liquids, mcvt)
