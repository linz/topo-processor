import pytest

from topo_processor.util import nzt_datetime_to_utc_datetime, quarterdate_to_date_string


def test_nzt_datetime_to_utc_datetime_daylight_saving_on():
    utc_date = nzt_datetime_to_utc_datetime("1988-01-11T00:00:00.000")
    assert utc_date.isoformat() == "1988-01-10T11:00:00+00:00"


def test_nzt_datetime_to_utc_datetime_daylight_saving_off():
    utc_date = nzt_datetime_to_utc_datetime("1988-07-11T00:00:00.000")
    assert utc_date.isoformat() == "1988-07-10T12:00:00+00:00"


def test_quarter_date_to_utc_correct_format():
    utc_date_string = quarterdate_to_date_string("2020/Q1")
    assert utc_date_string == "2019-12-31T11:00:00Z"


def test_quarter_date_to_utc_incorrect_format():
    returned_string = quarterdate_to_date_string("nzam_pilot")
    assert returned_string == "nzam_pilot"
