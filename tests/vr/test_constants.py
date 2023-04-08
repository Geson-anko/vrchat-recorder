from vrchat_recorder.vr import constants as mod


def test_header_versions():
    assert mod.HeaderVersions.V0 == "v0"


def test_header_names():
    assert mod.HeaderNames.VERSION == "version"
    assert mod.HeaderNames.BINARY_FORMAT == "binary_format"
