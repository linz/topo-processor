import asyncio
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.metadata.metadata_loaders.metadata_loader_imagery_historic import MetadataLoaderImageryHistoric
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


def test_is_applicable(setup):
    source_path = "test_abc.tiff"
    collection = setup
    item = Item(source_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert metadata_loader_imagery_historic.is_applicable(item)


def test_is_not_applicable_wrong_file_extension(setup):
    source_path = "test_abc"
    collection = setup
    item = Item(source_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert not metadata_loader_imagery_historic.is_applicable(item)


def test_is_not_applicable_wrong_data_type(setup):
    source_path = "test_abc.tiff"
    collection = setup
    collection.data_type = DataType.LidarDEM
    item = Item(source_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert not metadata_loader_imagery_historic.is_applicable(item)


def test_item_not_found_in_csv(setup):
    source_path = "test_abc.tiff"
    collection = setup
    item = Item(source_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    with pytest.raises(Exception, match=r"test_abc cannot be found in the csv."):
        asyncio.run(metadata_loader_imagery_historic.add_metadata(item))
