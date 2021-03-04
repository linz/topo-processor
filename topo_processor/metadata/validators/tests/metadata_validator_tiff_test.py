import asyncio
import os
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.metadata.validators.metadata_validator_tiff import MetadataValidatorTiff
from topo_processor.stac.collection import Collection
from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item


@pytest.fixture(autouse=True)
async def setup():
    """
    This function creates a temporary directory and deletes it after each test.
    See following link for details:
    https://docs.pytest.org/en/stable/fixture.html#yield-fixtures-recommended
    """
    temp_dir = mkdtemp()
    collection = Collection(DataType.ImageryHistoric, temp_dir)
    yield collection
    shutil.rmtree(temp_dir)


def test_check_validity(setup):
    tiff_path = os.path.join(os.getcwd(), "test_data", "tiffs", "399", "CROWN_399_E_49.tiff")
    collection = setup
    item = Item(tiff_path, collection)
    item.stac_item.properties.update({"linz:photo_type": "COLOUR"})

    validator = MetadataValidatorTiff()
    assert validator.is_applicable(item)
    with pytest.raises(Exception, match=r"Validation failed"):
        asyncio.run(validator.check_validity(item))
