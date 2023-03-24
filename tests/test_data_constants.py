from vrchat_recorder.data_constants import CSVHeaderNames, FileExtensions


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
