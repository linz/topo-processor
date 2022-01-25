import os

import pytest

from topo_processor.metadata.metadata_validators.metadata_validator_tiff import MetadataValidatorTiff
from topo_processor.stac.asset import Asset
from topo_processor.stac.item import Item


def test_check_validity() -> None:
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.add_asset(asset)
    item.linz_geospatial_type = "color image"
    asset.properties.update({"eo:bands": [{"name": "gray", "common_name": "pan"}]})

    validator = MetadataValidatorTiff()
    assert validator.is_applicable(item)
    with pytest.raises(Exception, match=r"Wrong linz_geospatial_type of 'color image' when bands = gray"):
        validator.validate_metadata(item)
