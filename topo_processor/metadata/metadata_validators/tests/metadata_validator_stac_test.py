import os
from datetime import datetime

import pystac.validation
import pytest
from pystac.errors import STACValidationError

from topo_processor.metadata.metadata_loaders.metadata_loader_imagery_historic import MetadataLoaderImageryHistoric
from topo_processor.metadata.metadata_validators.metadata_validator_stac import MetadataValidatorStac
from topo_processor.stac.asset import Asset
from topo_processor.stac.collection import Collection
from topo_processor.stac.item import Item
from topo_processor.stac.iter_errors_validator import IterErrorsValidator
from topo_processor.stac.linz_provider import LinzProviders
from topo_processor.stac.providers import Providers
from topo_processor.stac.stac_extensions import StacExtensions
from topo_processor.stac.validate_report import ValidateReport

# STAC item level tests


def test_check_validity_camera_extension() -> None:
    """check fails due to string"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"camera:nominal_focal_length": "string"})
    item.properties.update({"camera:sequence_number": 1234})
    item.add_extension(StacExtensions.camera.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_check_validity_film_extension() -> None:
    """check fails due to string"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"film:id": "1234"})
    item.properties.update({"film:negative_sequence": "string"})
    item.add_extension(StacExtensions.film.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_check_validity_fails_on_string_aerial_photo_extension() -> None:
    """check fails due to string in place of expected integer"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"aerial-photo:run": "string"})
    item.properties.update({"aerial-photo:altitude": "string"})
    item.properties.update({"aerial-photo:scale": 1234})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.properties.update({"aerial-photo:anomalies": ""})
    item.add_extension(StacExtensions.aerial_photo.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_check_validity_fails_on_required_field_aerial_photo_extension() -> None:
    """check fails due to missing required field"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"aerial-photo:altitude": 1234})
    item.properties.update({"aerial-photo:scale": 1234})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.properties.update({"aerial-photo:anomalies": "Cloud"})
    item.add_extension(StacExtensions.aerial_photo.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_check_validity_scanning_extension() -> None:
    """check fails due date string format"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"scan:is_original": True})
    item.properties.update({"scan:scanned": "string"})
    item.add_extension(StacExtensions.scanning.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_validate_metadata_with_report_item() -> None:
    """check that the method return a report of the errors for an item validation"""
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"film:id": "1234"})
    item.properties.update({"film:negative_sequence": "string"})
    item.add_extension(StacExtensions.film.value, add_to_collection=False)
    item.properties.update({"aerial-photo:altitude": 1234})
    item.properties.update({"aerial-photo:scale": 1234})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.properties.update({"aerial-photo:anomalies": "Cloud"})
    item.add_extension(StacExtensions.aerial_photo.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert '"string" is not of type "integer"' in validate_report.report_per_error_type[StacExtensions.film.value]
    assert (
        '"aerial-photo:run" is a required property' in validate_report.report_per_error_type[StacExtensions.aerial_photo.value]
    )


def test_check_validity_version_extension() -> None:
    """check fails due to missing version"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.datetime = datetime.now()
    item.properties.pop("version")
    item.add_asset(asset)
    item.add_extension(StacExtensions.version.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)


def test_check_multiple_stac_extensions_default_pystac_validator() -> None:
    """check should raise STACValidationError only for first extension"""
    pystac.validation.set_validator(pystac.validation.stac_validator.JsonSchemaSTACValidator())
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"aerial-photo:run": "string"})
    item.properties.update({"aerial-photo:altitude": "string"})
    item.properties.update({"aerial-photo:scale": 1234})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.properties.update({"aerial-photo:anomalies": ""})
    item.properties.update({"camera:nominal_focal_length": "string"})
    item.properties.update({"camera:sequence_number": 1234})
    item.add_extension(StacExtensions.aerial_photo.value, add_to_collection=False)
    item.add_extension(StacExtensions.camera.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert isinstance(
        pystac.validation.RegisteredValidator.get_validator(), pystac.validation.stac_validator.JsonSchemaSTACValidator
    )
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError) as e:
        validator.validate_metadata(item)
    assert "aerial-photo" in str(e.value)
    assert not "camera" in str(e.value)


def test_check_multiple_stac_extensions_custom_iter_validator() -> None:
    """check should raise STACValidationError for both extensions"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"aerial-photo:run": "string"})
    item.properties.update({"aerial-photo:altitude": "string"})
    item.properties.update({"aerial-photo:scale": 1234})
    item.properties.update({"aerial-photo:sequence_number": 1234})
    item.properties.update({"aerial-photo:anomalies": ""})
    item.properties.update({"camera:nominal_focal_length": "string"})
    item.properties.update({"camera:sequence_number": 1234})
    item.add_extension(StacExtensions.aerial_photo.value, add_to_collection=False)
    item.add_extension(StacExtensions.camera.value, add_to_collection=False)
    validator = MetadataValidatorStac()
    assert isinstance(pystac.validation.RegisteredValidator.get_validator(), IterErrorsValidator)
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError) as e:
        validator.validate_metadata(item)
    assert "aerial-photo" in str(e.value)
    assert "camera" in str(e.value)


# STAC collection level tests


def test_validate_collection_with_summaries_iter_validator(setup: str) -> None:
    target = setup
    collection = Collection("AUCKLAND 1")
    collection.description = "fake_description"
    collection.license = "face_license"
    collection.survey = "SURVEY_1"
    collection.add_linz_provider(LinzProviders.LTTW.value)
    collection.add_linz_provider(LinzProviders.LMPP.value)
    collection.extra_fields.update(
        {
            "linz:lifecycle": "completed",
            "linz:history": "LINZ and its predecessors, Lands & Survey and Department of Survey and Land Information (DOSLI), commissioned aerial photography for the Crown between 1936 and 2008.",
            "quality:description": "The spatial extents provided are only an approximate coverage for the ungeoreferenced aerial photographs.",
        }
    )
    test_geom = {
        "WKT": "POLYGON ((177.168157744315 -38.7538525409217,"
        "177.23423558687 -38.7514276946524,"
        "177.237358655351 -38.8031681573174,"
        "177.17123348276 -38.8055953066942,"
        "177.168157744315 -38.7538525409217))"
    }
    test_datetime = datetime.strptime("1918-11-11", "%Y-%m-%d")

    item_1 = Item("item_1_id")
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_spatial_extent(item_1, asset_metadata=test_geom)
    item_1.datetime = test_datetime
    item_1.properties = {
        "mission": "SURVEY_1",
        "proj:centroid": {"lat": -45.8079, "lon": 170.5548},
        "camera:sequence_number": 89555,
        "film:id": "731",
        "aerial-photo:scale": 6600,
        "scan:scanned": "2014-06-30T12:00:00Z",
        "proj:epsg": "null",
    }
    collection.add_item(item_1)
    item_1.collection = collection
    stac_item_1 = item_1.create_stac()

    item_2 = Item("item_2_id")
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_spatial_extent(item_2, asset_metadata=test_geom)
    item_2.datetime = test_datetime
    item_2.properties = {
        "mission": "SURVEY_1",
        "proj:centroid": {"lat": -45.8079, "lon": 170.5599},
        "camera:sequence_number": 89554,
        "film:id": "731",
        "aerial-photo:scale": 5600,
        "scan:scanned": "2019-12-31T11:00:00Z",
        "proj:epsg": "null",
    }
    collection.add_item(item_2)
    item_2.collection = collection
    stac_item_2 = item_2.create_stac()

    collection.add_extension(StacExtensions.historical_imagery.value)
    collection.add_extension(StacExtensions.linz.value)
    collection.add_extension(StacExtensions.quality.value)
    collection.add_extension(StacExtensions.aerial_photo.value)
    collection.add_extension(StacExtensions.camera.value)
    collection.add_extension(StacExtensions.film.value)
    collection.add_extension(StacExtensions.scanning.value)
    collection.add_extension(StacExtensions.eo.value)
    collection.add_extension(StacExtensions.file.value)
    collection.add_extension(StacExtensions.projection.value)
    collection.add_extension(StacExtensions.version.value)

    pystac_collection = collection.create_stac()

    validator = MetadataValidatorStac()
    pystac_collection = item_1.collection.create_stac()
    pystac_collection.add_item(stac_item_1)
    pystac_collection.add_item(stac_item_2)
    collection.generate_summaries(pystac_collection)

    assert isinstance(pystac.validation.RegisteredValidator.get_validator(), IterErrorsValidator)
    assert validator.is_applicable(collection)
    with pytest.raises(STACValidationError) as e:
        validator.validate_metadata_pystac_collection(pystac_collection)
    assert not "summaries" in str(e.value)
    assert "linz/schema.json" in str(e.value)
    assert "film/schema.json" in str(e.value)
    assert "aerial-photo:run" in str(e.value)
    assert "aerial-photo:sequence_number" in str(e.value)


def test_validate_metadata_with_report_collection() -> None:
    """check that the method return a report of the errors for a collection validation"""
    validate_report: ValidateReport = ValidateReport()
    collection = Collection("title_col")
    collection.description = "desc"
    collection.license = "lic"
    validator = MetadataValidatorStac()
    assert validator.is_applicable(collection)
    validate_report.add_errors(validator.validate_metadata_with_report(collection))
    assert validate_report.total == 1
    assert not validate_report.report_per_error_type


def test_validate_metadata_linz_with_report_collection(mocker) -> None:  # type: ignore
    """check that the linz collection schema validates"""
    validate_report: ValidateReport = ValidateReport()
    collection = Collection("title_col")
    collection.description = "desc"
    collection.license = "lic"
    collection.extra_fields.update(
        {
            "linz:lifecycle": "completed",
            "linz:history": "LINZ and its predecessors, Lands & Survey and Department of Survey and Land Information (DOSLI), commissioned aerial photography for the Crown between 1936 and 2008.",
            "quality:description": "The spatial extents provided are only an approximate coverage for the ungeoreferenced aerial photographs.",
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
            "processing:software": [{"Topo Processor": "v0.1.0"}, {"Topo Processor": "v0.3.0"}],
            "created": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-01-01T00:00:00Z"},
            "updated": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-03-01T00:00:00Z"},
        },
    )
    collection.add_extension(StacExtensions.linz.value)
    collection.add_extension(StacExtensions.quality.value)
    collection.add_extension(StacExtensions.file.value)
    collection.add_extension(StacExtensions.projection.value)
    collection.add_extension(StacExtensions.version.value)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(collection)
    validate_report.add_errors(validator.validate_metadata_with_report(collection))
    assert not validate_report.report_per_error_type


def test_validate_metadata_linz_collection_missing_linz_fields(mocker) -> None:  # type: ignore
    """check that the linz collection schema gives error missing linz fields"""
    validate_report: ValidateReport = ValidateReport()
    collection = Collection("title_col")
    collection.description = "desc"
    collection.license = "lic"
    collection.extra_fields.update(
        {
            "version": "1",
        }
    )
    collection.add_provider(Providers.NZAM.value)
    mocker.patch("topo_processor.stac.collection.Collection.get_linz_geospatial_type", return_value="black and white image")
    mocker.patch(
        "topo_processor.stac.collection.Collection.get_linz_asset_summaries",
        return_value={
            "processing:software": [{"Topo Processor": "v0.1.0"}, {"Topo Processor": "v0.3.0"}],
            "created": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-01-01T00:00:00Z"},
            "updated": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-03-01T00:00:00Z"},
        },
    )
    collection.extra_fields.pop("linz:security_classification")
    collection.add_extension(StacExtensions.linz.value)
    collection.add_extension(StacExtensions.quality.value)
    collection.add_extension(StacExtensions.file.value)
    collection.add_extension(StacExtensions.projection.value)
    collection.add_extension(StacExtensions.version.value)
    validator = MetadataValidatorStac()
    assert validator.is_applicable(collection)
    validate_report.add_errors(validator.validate_metadata_with_report(collection))
    assert '"linz:lifecycle" is a required property' in validate_report.report_per_error_type[StacExtensions.linz.value]
    assert '"linz:history" is a required property' in validate_report.report_per_error_type[StacExtensions.linz.value]
    assert (
        '"linz:security_classification" is a required property'
        in validate_report.report_per_error_type[StacExtensions.linz.value]
    )
    assert '"linz:providers" is a required property' in validate_report.report_per_error_type[StacExtensions.linz.value]


# Local schema file tests


@pytest.mark.skip(reason="use this test for local schema testing - multiple errors in report")
def test_validate_metadata_with_report_item_local() -> None:
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
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
def test_check_validity_local_film_extension() -> None:
    source = "file://" + os.getcwd() + "/test_data" + "/schemas"
    validate_report: ValidateReport = ValidateReport()
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.datetime = datetime.now()
    item.add_asset(asset)
    item.properties.update({"film:id": "1234"})
    item.properties.update({"film:negative_sequence": 1234})
    item.add_extension(source + "/" + "film-schema.json")
    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    validate_report.add_errors(validator.validate_metadata_with_report(item))
    assert not validate_report.report_per_error_type
