import os
from logging import error

import pytest

from topo_processor.stac.validate_report import ValidateReport


def test_increment_error():
    """"""
    error_report: ValidateReport = ValidateReport()
    error_report.increment_error("schema_a", "error_1")
    assert error_report.report_per_error_type["schema_a"]["error_1"] == 1
    error_report.increment_error("schema_a", "error_1")
    assert error_report.report_per_error_type["schema_a"]["error_1"] == 2
    error_report.increment_error("schema_b", "error_1")
    assert error_report.report_per_error_type["schema_b"]["error_1"] == 1
    error_report.increment_error("schema_a", "error_2")
    assert error_report.report_per_error_type["schema_a"]["error_2"] == 1
