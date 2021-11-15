import pytest

from topo_processor.util.configuration import configuration


def test_configuration():
    assert configuration["LDS_CACHE_LOCAL_TMP_FOLDER"] == "temp"
