import os
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.stac import add_asset_image
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


@pytest.mark.asyncio
async def test_add_asset_image(setup):
    tiff_path = os.path.join(os.getcwd(), "test_data", "tiffs", "399", "CROWN_399_E_49.tiff")
    collection = setup
    item = Item(tiff_path, collection)
    item.asset_basename = "399/72359"
    item.asset_extension = "lzw.cog.tiff"
    await add_asset_image(item)
    assert len(item.stac_item.assets) == 1
