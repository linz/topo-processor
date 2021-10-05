import os

import pytest
from pystac.errors import STACValidationError

from topo_processor.metadata.metadata_validators.metadata_validator_stac import MetadataValidatorStac
from topo_processor.stac import Asset, Item
from topo_processor.stac.stac_extensions import StacExtensions


def test_check_validity():
    """check fails due to string"""
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.add_asset(asset)
    item.properties.update({"camera:nominal_focal_length": "string"})
    item.properties.update({"camera:sequence_number": 1234})
    item.add_extension(StacExtensions.camera.value)

    validator = MetadataValidatorStac()
    assert validator.is_applicable(item)
    with pytest.raises(STACValidationError):
        validator.validate_metadata(item)
