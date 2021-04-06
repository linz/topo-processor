import os

import pytest

from topo_processor.metadata.metadata_validators.metadata_validator_tiff import MetadataValidatorTiff
from topo_processor.stac import Asset, Item


@pytest.mark.asyncio
async def test_check_validity():
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "399", "CROWN_399_E_49.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.add_asset(asset)
    item.properties.update({"linz:photo_type": "COLOUR"})

    validator = MetadataValidatorTiff()
    assert validator.is_applicable(item)
    with pytest.raises(Exception, match=r"Wrong photo type of gray"):
        await validator.validate_metadata(item)
