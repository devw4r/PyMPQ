from enum import IntEnum


class CustomErrors(IntEnum):
    NO_WOW_PATH = 1
    INVALID_WOW_PATH = 2
    NO_WOW_DATA_PATH = 3
    NO_DBC_PATH_FOUND = 4
    UNABLE_TO_EXTRACT_MAP_DBC = 5
    NO_DBC_MAPS_LOCATED = 6

