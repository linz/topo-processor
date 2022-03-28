import os
from datetime import datetime

import pystac
import pytest
from pystac import STACValidationError

from topo_processor.metadata.metadata_validators.metadata_validator_stac import MetadataValidatorStac
from topo_processor.stac.asset import Asset
from topo_processor.stac.item import Item
from topo_processor.stac.iter_errors_validator import IterErrorsValidator
from topo_processor.stac.stac_extensions import StacExtensions


def test_iter_errors_validator() -> None:
    """check error details is in exception message"""
    pystac.validation.set_validator(IterErrorsValidator())
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
    with pytest.raises(STACValidationError) as e:
        validator.validate_metadata(item)
    assert "'string' is not of type 'integer'" in str(e.value)
