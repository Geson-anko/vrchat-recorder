import pytest

from vrchat_recorder.data_constants import (
    CSVHeaderNames,
    DataTypeNames,
    FileExtensions,
    get_data_type_name,
)


def test_CSVHeaderNames():
    assert CSVHeaderNames.TIMESTAMP == "timestamp"
    assert CSVHeaderNames.PARAMETER_NAME == "parameter_name"
    assert CSVHeaderNames.DATA_TYPE == "data_type"
    assert CSVHeaderNames.VALUE == "value"


def test_FileExtensions():
    assert FileExtensions.VRCREC == "vrcrec"
    assert FileExtensions.CSV == "csv"
    assert FileExtensions.OSCFEEDBACK == "oscfb"
    assert FileExtensions.CONTROLLER == "ctrlr"


def test_DataTypeNames():
    assert DataTypeNames.FLOAT == "float"
    assert DataTypeNames.INT == "int"
    assert DataTypeNames.BOOL == "bool"
    assert DataTypeNames.STRING == "str"


@pytest.mark.parametrize(
    ["obj", "expected"],
    [
        (1.0, DataTypeNames.FLOAT),
        (1, DataTypeNames.INT),
        (True, DataTypeNames.BOOL),
        ("test", DataTypeNames.STRING),
        ([1, 2, 3], str(type([1, 2, 3]))),
        ({1: 2, 3: 4}, str(type({1: 2, 3: 4}))),
        (None, str(type(None))),
    ],
)
def test_get_data_type_name(obj, expected):
    assert get_data_type_name(obj) == expected
