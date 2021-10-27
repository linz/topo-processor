import pytest

from topo_processor.util import nzt_datetime_to_utc_datetime

def test_nzt_datetime_to_utc_datetime():
    utc_date = nzt_datetime_to_utc_datetime('1988-01-11T00:00:00.000')
    assert utc_date.isoformat() == '1988-01-10T11:00:00+00:00'
