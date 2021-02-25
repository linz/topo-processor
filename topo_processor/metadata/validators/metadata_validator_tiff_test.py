import asyncio
import os

import pytest

from topo_processor.stac.collection import Collection
from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item

from .metadata_validator_tiff import MetadataValidatorTiff


def test_check_validity():
    tiff_path = os.path.join(os.getcwd(), "test_data", "tiffs", "399", "CROWN_399_E_49.tiff")
    collection = Collection(DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    item.stac_item.properties.update({"linz:photo_type": "COLOUR"})

    validator = MetadataValidatorTiff()
    assert validator.is_applicable(item)
    with pytest.raises(Exception, match=r"Validation failed"):
        asyncio.run(validator.check_validity(item))
