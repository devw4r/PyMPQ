import os
import sys

from pydbclib.DbcReader import DbcReader
from pympqlib.MpqArchive import MpqArchive
from pydbclib.structs.DbcMapAlpha import DbcMapAlpha
from definitions.enums.CustomErrors import CustomErrors


ROOT_PATH = ''
DATA_FOLDER = 'Data'
DBC_NEEDED = 'dbc.MPQ'
DBC_PATH = ''
DATA_PATH = ''
DBC_MAPS = []

if __name__ == '__main__':
    # Parse args.
    for i, arg in enumerate(sys.argv):
        if '-d' in arg:
            ROOT_PATH = sys.argv[i + 1]

    # Validate WoW root provided.
    if not ROOT_PATH:
        print('No wow root path provided. (World of Warcraft base directory)')
        exit(CustomErrors.NO_WOW_PATH)
    # Validate its existence.
    elif not os.path.exists(ROOT_PATH):
        print(f'Data path "{ROOT_PATH}" does not exist.')
        exit(CustomErrors.INVALID_WOW_PATH)

    # Validate /Data/.
    DATA_PATH = os.path.join(ROOT_PATH, DATA_FOLDER)
    if not os.path.exists(DATA_PATH):
        print(f'Unable to locate {DATA_PATH}.')
        exit(CustomErrors.NO_WOW_DATA_PATH)

    # Validate dbc.MPQ.
    DBC_PATH = os.path.join(DATA_PATH, DBC_NEEDED)
    if not os.path.exists(DBC_PATH):
        print(f'Unable to locate {DBC_PATH}.')
        exit(CustomErrors.NO_DBC_PATH_FOUND)

    # Extract available maps at Map.dbc.
    with MpqArchive(DBC_PATH) as archive:
        map_dbc = archive.find_file('Map.dbc')
        if not map_dbc:
            print(f'Unable to extract Map.dbc')
            exit(CustomErrors.UNABLE_TO_EXTRACT_MAP_DBC)
        # Read records as DbcMapAlpha.
        with DbcReader(buffer=archive.read_file_bytes(map_dbc)) as dbc_reader:
            DBC_MAPS = dbc_reader.read_records_by_type(DbcMapAlpha)

    # Validate we have maps.
    if not DBC_MAPS:
        print(f'Unable to extract maps from {DBC_PATH}.')
        exit(CustomErrors.NO_DBC_MAPS_LOCATED)
    else:
        print(f'Found {len(DBC_MAPS)} dbc maps.')

