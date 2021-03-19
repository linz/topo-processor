import asyncio
import os
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.metadata.metadata_loaders.metadata_loader_tiff import MetadataLoaderTiff
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
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.mark.asyncio
async def test_add_metadata(setup):
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "399", "CROWN_399_E_49.tiff")
    temp_dir = setup
    item = Item(source_path, DataType.ImageryHistoric, "fake_target", temp_dir)
    loader = MetadataLoaderTiff()
    assert loader.is_applicable(item)

    await loader.add_metadata(item)
    assert item.properties["proj:epsg"] is None
    assert len(item.assets) == 1
