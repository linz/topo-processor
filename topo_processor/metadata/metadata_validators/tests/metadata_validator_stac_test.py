import os
from datetime import datetime

import pytest
from pystac.errors import STACValidationError

import topo_processor.stac as stac
from topo_processor.metadata.metadata_validators.metadata_validator_stac import MetadataValidatorStac
from topo_processor.stac.linz_provider import LinzProviders
from topo_processor.stac.providers import Providers
from topo_processor.stac.validate_report import ValidateReport

# STAC item level tests


def test_check_validity_camera_extension():
    """check fails due to string"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"camera:nominal_focal_length": "string"})
    item.properties.update({"camera:sequence_number": 1234})
    item.add_extension(stac.StacExtensions.camera.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_check_validity_film_extension():
    """check fails due to string"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"film:id": "1234"})
    item.properties.update({"film:negative_sequence": "string"})
    item.add_extension(stac.StacExtensions.film.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


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
    item.add_extension(stac.StacExtensions.aerial_photo.value, add_to_collection=False)
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
    item.add_extension(stac.StacExtensions.aerial_photo.value, add_to_collection=False)
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
    item.add_extension(stac.StacExtensions.scanning.value, add_to_collection=False)
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
    item.add_extension(stac.StacExtensions.film.value, add_to_collection=False)
    item.properties.update({"aerial-photo:altitude": 1234})
    item.properties.update({"aerial-photo:scale": 1234})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.properties.update({"aerial-photo:anomalies": "Cloud"})
    item.add_extension(stac.StacExtensions.aerial_photo.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert '"string" is not of type "integer"' in validate_report.report_per_error_type[stac.StacExtensions.film.value]
    assert (
        '"aerial-photo:run" is a required property'
        in validate_report.report_per_error_type[stac.StacExtensions.aerial_photo.value]
    )


def test_check_validity_version_extension():
    """check fails due to missing version"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.properties.pop("version")
    item.add_asset(asset)
    item.add_extension(stac.StacExtensions.version.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_check_validity_processing_extension():
    """check validates item processing:software"""
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"processing:software": {"Topo Processor": "0.1.0"}})
    item.add_extension(stac.StacExtensions.processing.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert not validate_report.report_per_error_type


# STAC collection level tests


def test_validate_metadata_with_report_collection():
    """check that the method return a report of the errors for a collection validation"""
    validate_report: ValidateReport = ValidateReport()
    collection = stac.Collection("title_col")
    collection.description = "desc"
    collection.license = "lic"
    validator = MetadataValidatorStac()
    assert validator.is_applicable(collection)
    validate_report.add_errors(validator.validate_metadata_with_report(collection))
    assert validate_report.total == 1
    assert not validate_report.report_per_error_type


def test_validate_metadata_linz_collection(mocker):
    """check that the linz collection schema validates"""
    validate_report: ValidateReport = ValidateReport()
    collection = stac.Collection("title_col")
    collection.description = "desc"
    collection.license = "lic"
    collection.extra_fields.update(
        {
            "linz:lifecycle": "completed",
            "linz:history": "LINZ and its predecessors, Lands & Survey and Department of Survey and Land Information (DOSLI), commissioned aerial photography for the Crown between 1936 and 2008.",
            "processing:software": {"Topo Processor": "0.1.0"},
            "version": "1",
        }
    )
    collection.add_provider(Providers.NZAM.value)
    collection.add_linz_provider(LinzProviders.LTTW.value)
    collection.add_linz_provider(LinzProviders.LMPP.value)
    mocker.patch("topo_processor.stac.collection.Collection.get_linz_geospatial_type", return_value="black and white image")
    mocker.patch(
        "topo_processor.stac.collection.Collection.get_linz_asset_summaries",
        return_value={
            "created": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-01-01T00:00:00Z"},
            "updated": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-03-01T00:00:00Z"},
        },
    )
    collection.add_extension(stac.StacExtensions.linz.value)
    collection.add_extension(stac.StacExtensions.quality.value)
    collection.add_extension(stac.StacExtensions.file.value)
    collection.add_extension(stac.StacExtensions.projection.value)
    collection.add_extension(stac.StacExtensions.version.value)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(collection)
    validate_report.add_errors(validator.validate_metadata_with_report(collection))
    assert not validate_report.report_per_error_type


def test_validate_metadata_linz_collection_missing_linz_fields(mocker):
    """check that the linz collection schema gives error missing linz fields"""
    validate_report: ValidateReport = ValidateReport()
    collection = stac.Collection("title_col")
    collection.description = "desc"
    collection.license = "lic"
    collection.extra_fields.update(
        {
            "processing:software": {"Topo Processor": "0.1.0"},
            "version": "1",
        }
    )
    collection.add_provider(Providers.NZAM.value)
    mocker.patch("topo_processor.stac.collection.Collection.get_linz_geospatial_type", return_value="black and white image")
    mocker.patch(
        "topo_processor.stac.collection.Collection.get_linz_asset_summaries",
        return_value={
            "created": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-01-01T00:00:00Z"},
            "updated": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-03-01T00:00:00Z"},
        },
    )
    collection.extra_fields.pop("linz:security_classification")
    collection.add_extension(stac.StacExtensions.linz.value)
    collection.add_extension(stac.StacExtensions.quality.value)
    collection.add_extension(stac.StacExtensions.file.value)
    collection.add_extension(stac.StacExtensions.projection.value)
    collection.add_extension(stac.StacExtensions.version.value)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(collection)
    validate_report.add_errors(validator.validate_metadata_with_report(collection))
    assert '"linz:lifecycle" is a required property' in validate_report.report_per_error_type[stac.StacExtensions.linz.value]
    assert '"linz:history" is a required property' in validate_report.report_per_error_type[stac.StacExtensions.linz.value]
    assert (
        '"linz:security_classification" is a required property'
        in validate_report.report_per_error_type[stac.StacExtensions.linz.value]
    )
    assert '"linz:providers" is a required property' in validate_report.report_per_error_type[stac.StacExtensions.linz.value]


# Local schema file tests


@pytest.mark.skip(reason="use this test for local schema testing - multiple errors in report")
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


@pytest.mark.skip(reason="use this test for local schema testing - film item")
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
