from pydbclib.DbcReader import DbcReader
from pydbclib.structs.DbcMap import DbcMap
from pympqlib.MpqArchive import MpqArchive

if __name__ == '__main__':
    with DbcReader('Map.dbc') as dbc:
        for i in range(0, dbc.header.record_count):
            dbc_map = dbc.read(DbcMap)
            print(dbc_map.name_en_us)

    with MpqArchive('/home/user/.wine/drive_c/Program Files (x86)/WoW/Data/dbc.MPQ') as archive:
        for i, entry in enumerate(archive.mpq_entries):
            try:
                file_bytes = archive.read_file_bytes(entry)
                if not file_bytes:
                    continue
                with open(f'./out/{entry.filename}', 'wb') as f:
                    f.write(file_bytes)
            except:
                print(f'Skipped entry {i}, no filename.')
