"""This class contains all the data constants used in the program."""
from typing import Any


class CSVHeaderNames:
    """This class contains all the header names for the CSV files."""

    TIMESTAMP = "timestamp"
    EVENT_TYPE = "event_type"
    PARAMETER_NAME = "parameter_name"
    DATA_TYPE = "data_type"
    VALUE = "value"
    CONTROLLER_ROLE = "controller_role"
    BUTTON_ID = "button_id"
    AGE_SECONDS = "age_seconds"


class FileExtensions:
    """This class contains all the file extensions used in the program."""

    VRCREC = "vrcrec"
    CSV = "csv"
    OSCFEEDBACK = "oscfb"
    CONTROLLER = "ctrlr"
    VIDEO = "video"
    GAMEPAD = "gamepad"
    WAV = "wav"
    MICROPHONE = "mic"
    SPEAKER = "speaker"


class DataTypeNames:
    """This class contains all data type names used in the recording."""

    FLOAT = "float"
    INT = "int"
    BOOL = "bool"
    STRING = "str"


def get_data_type_name(obj: Any) -> str:
    """Get the data type name of the given object.

    Args:
        obj (Any): The object.

    Returns:
        str: The data type name of the given object.
    """
    if isinstance(obj, float):
        return DataTypeNames.FLOAT
    elif isinstance(obj, bool):
        return DataTypeNames.BOOL
    elif isinstance(obj, int):
        return DataTypeNames.INT
    elif isinstance(obj, str):
        return DataTypeNames.STRING
    else:
        return str(type(obj))
