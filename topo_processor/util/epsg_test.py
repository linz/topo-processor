import pytest

from .epsg import epsg_code

def test_epsg_code():
    assert epsg_code("EPSG:2193") == 2193
    assert epsg_code("2012") == 2012

def test_epsg_code_exception():
    with pytest.raises(Exception, match=r"EPSG:not_a_code is not a valid EPSG code"):
        epsg_code("EPSG:not_a_code")
    with pytest.raises(Exception, match=r"9999999 is not a valid EPSG code"):
        epsg_code("9999999")
