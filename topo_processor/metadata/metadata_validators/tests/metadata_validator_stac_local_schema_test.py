import os
from datetime import datetime

import pytest

import topo_processor.stac as stac
from topo_processor.metadata.metadata_validators.metadata_validator_stac import MetadataValidatorStac
from topo_processor.stac.linz_provider import LinzProviders
from topo_processor.stac.providers import Providers
from topo_processor.stac.validate_report import ValidateReport


@pytest.mark.skip(reason="use this test for local schema testing")
def test_validate_metadata_with_report_item_local():
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"film:id": "1234"})
    item.properties.update({"film:negative_sequence": "string"})
    item.properties.update({"aerial-photo:altitude": 1234})
    item.properties.update({"aerial-photo:scale": 1234})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.properties.update({"aerial-photo:anomalies": "Cloud"})
    item.add_extension(source + "/" + "film-schema.json")
    item.add_extension(source + "/" + "aerial-photo-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert '"string" is not of type "integer"' in validate_report.report_per_error_type[source + "/" + "film-schema.json"]
    assert (
        '"aerial-photo:run" is a required property'
        in validate_report.report_per_error_type[source + "/" + "aerial-photo-schema.json"]
    )


@pytest.mark.skip(reason="use this test for local schema testing")
def test_validate_metadata_with_report_item_hi_local():
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"mission": "string"})
    item.properties.update({"platform": "string"})
    item.add_extension(source + "/" + "hi-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert not validate_report.report_per_error_type


@pytest.mark.skip(reason="use this test for local schema testing")
def test_check_validity_local_film_extension():
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"film:id": "1234"})
    item.properties.update({"film:negative_sequence": 1234})
    item.add_extension(source + "/" + "film-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert not validate_report.report_per_error_type


@pytest.mark.skip(reason="use this test for local schema testing")
def test_check_validity_local_aerial_photo_extension():
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"aerial-photo:run": "1234"})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.add_extension(source + "/" + "aerial-photo-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert not validate_report.report_per_error_type


@pytest.mark.skip(reason="use this test for local schema testing")
def test_check_validity_local_camera_extension():
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"camera:nominal_focal_length": 1234})
    item.properties.update({"camera:sequence_number": 1234})
    item.add_extension(source + "/" + "camera-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert not validate_report.report_per_error_type


@pytest.mark.skip(reason="use this test for local schema testing")
def test_check_validity_local_scanning_extension():
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"scan:is_original": True})
    item.properties.update({"scan:scanned": "2018-09-30T11:00:00Z"})
    item.add_extension(source + "/" + "scanning-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert not validate_report.report_per_error_type


@pytest.mark.skip(reason="use this test for local schema testing")
def test_validate_against_local_schema_film():
    """check that the method return a report of the errors for an item validation"""
    # https://datatracker.ietf.org/doc/html/rfc8089#appendix-B
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"film:id": "1234"})
    item.properties.update({"film:negative_sequence": "string"})
    item.add_extension(source + "/" + "film-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert '"string" is not of type "integer"' in validate_report.report_per_error_type[source + "/" + "film-schema.json"]


@pytest.mark.skip(reason="use this test for local schema testing")
def test_validate_against_local_schema_aerial():
    """check that the method return a report of the errors for an item validation"""
    # https://datatracker.ietf.org/doc/html/rfc8089#appendix-B
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"aerial-photo:run": "1234"})
    item.properties.update({"aerial-photo:sequence_number": "string"})
    item.add_extension(source + "/" + "aerial-photo-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert (
        '"string" is not of type "integer"' in validate_report.report_per_error_type[source + "/" + "aerial-photo-schema.json"]
    )


@pytest.mark.skip(reason="use this test for local schema testing")
def test_validate_against_local_schema_camera():
    """check that the method return a report of the errors for an item validation"""
    # https://datatracker.ietf.org/doc/html/rfc8089#appendix-B
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"camera:nominal_focal_length": 1234})
    item.properties.update({"camera:sequence_number": "string"})
    item.add_extension(source + "/" + "camera-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert '"string" is not of type "integer"' in validate_report.report_per_error_type[source + "/" + "camera-schema.json"]


@pytest.mark.skip(reason="use this test for local schema testing")
def test_validate_against_local_schema_scanning_boolean():
    """check that the method return a report of the errors for an item validation"""
    # https://datatracker.ietf.org/doc/html/rfc8089#appendix-B
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"scan:is_original": "string"})
    item.properties.update({"scan:scanned": "2018-09-30T11:00:00Z"})
    item.add_extension(source + "/" + "scanning-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert '"string" is not of type "boolean"' in validate_report.report_per_error_type[source + "/" + "scanning-schema.json"]


@pytest.mark.skip(reason="use this test for local schema testing")
def test_validate_against_local_schema_scanning_date():
    """check that the method return a report of the errors for an item validation"""
    # https://datatracker.ietf.org/doc/html/rfc8089#appendix-B
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"scan:is_original": True})
    item.properties.update({"scan:scanned": "string"})
    item.add_extension(source + "/" + "scanning-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert (
        '"string" does not match "(\\+00:00|Z)$"'
        in validate_report.report_per_error_type[source + "/" + "scanning-schema.json"]
    )
