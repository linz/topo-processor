import asyncio
import os
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.metadata.metadata_loaders.metadata_loader_tiff import MetadataLoaderTiff
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


def test_add_metadata(setup):
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "399", "CROWN_399_E_49.tiff")
    collection = setup
    item = Item(source_path, collection)
    item.asset_basename = "399/1234"
    loader = MetadataLoaderTiff()
    assert loader.is_applicable(item)

    asyncio.run(loader.add_metadata(item))
    assert item.stac_item.properties["proj:epsg"] is None
    assert len(item.stac_item.assets) == 0
