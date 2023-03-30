from unittest.mock import MagicMock

import openvr
import pytest


@pytest.fixture
def mock_vrsystem():
    return MagicMock(spec=openvr.IVRSystem)
