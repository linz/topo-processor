import pytest
from pystac.errors import STACValidationError

import topo_processor.stac as stac
from topo_processor.metadata.metadata_validators.metadata_validator_stac import MetadataValidatorStac
from topo_processor.stac.linz_provider import LinzProviders
from topo_processor.stac.providers import Providers
from topo_processor.stac.validate_report import ValidateReport


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
