import os
from datetime import datetime
from typing import Dict

import pytest
from pystac.errors import STACValidationError

import topo_processor.stac as stac
from topo_processor.metadata.metadata_validators.metadata_validator_stac import MetadataValidatorStac
from topo_processor.stac.validate_report import ValidateReport


def test_check_validity_camera_extension():
    """check fails due to string"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"camera:nominal_focal_length": "string"})
    item.properties.update({"camera:sequence_number": 1234})
    item.add_extension(stac.StacExtensions.camera.value)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_check_validity_film_extension():
    """check fails due to string"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.add_asset(asset)
    item.properties.update({"film:id": "1234"})
    item.properties.update({"film:negative_sequence": "string"})
    item.add_extension(stac.StacExtensions.film.value)


def test_check_validity_fails_on_string_aerial_photo_extension():
    """check fails due to string in place of expected integer"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"aerial-photo:run": "string"})
    item.properties.update({"aerial-photo:altitude": "string"})
    item.properties.update({"aerial-photo:scale": 1234})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.properties.update({"aerial-photo:anomalies": ""})
    item.add_extension(stac.StacExtensions.aerial_photo.value)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_check_validity_fails_on_required_field_aerial_photo_extension():
    """check fails due to missing required field"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"aerial-photo:altitude": 1234})
    item.properties.update({"aerial-photo:scale": 1234})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.properties.update({"aerial-photo:anomalies": "Cloud"})
    item.add_extension(stac.StacExtensions.aerial_photo.value)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_check_validity_scanning_extension():
    """check fails due date string format"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"scan:is_original": True})
    item.properties.update({"scan:scanned": "string"})
    item.add_extension(stac.StacExtensions.scanning.value)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_validate_metadata_with_report_item():
    """check that the method return a report of the errors for an item validation"""
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"film:id": "1234"})
    item.properties.update({"film:negative_sequence": "string"})
    item.add_extension(stac.StacExtensions.film.value)
    item.properties.update({"aerial-photo:altitude": 1234})
    item.properties.update({"aerial-photo:scale": 1234})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.properties.update({"aerial-photo:anomalies": "Cloud"})
    item.add_extension(stac.StacExtensions.aerial_photo.value)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert '"string" is not of type "integer"' in validate_report.report_per_error_type[stac.StacExtensions.film.value]
    assert (
        '"aerial-photo:run" is a required property'
        in validate_report.report_per_error_type[stac.StacExtensions.aerial_photo.value]
    )


def test_validate_metadata_with_report_collection():
    """check that the method return a report of the errors for a collection validation"""
    """check that the method return a report of the errors for an item validation"""
    validate_report: ValidateReport = ValidateReport()
    collection = stac.Collection("title_col")
    collection.description = "desc"
    collection.license = "lic"
    validator = MetadataValidatorStac()
    assert validator.is_applicable(collection)
    validate_report.add_errors(validator.validate_metadata_with_report(collection))
    assert validate_report.total == 1
    assert not validate_report.report_per_error_type


def test_validate_against_local_schema():
    """check that the method return a report of the errors for an item validation"""
    source = os.path.join(os.getcwd(), "test_data", "schemas")
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
