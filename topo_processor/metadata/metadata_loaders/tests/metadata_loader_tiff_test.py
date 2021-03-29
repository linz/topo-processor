import os

import pytest

from topo_processor.metadata.metadata_loaders.metadata_loader_tiff import MetadataLoaderTiff
from topo_processor.stac import Asset, Item


@pytest.mark.asyncio
async def test_load_metadata():
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "399", "CROWN_399_E_49.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.add_asset(asset)
    loader = MetadataLoaderTiff()
    assert loader.is_applicable(asset)

    await loader.load_metadata(asset)
    assert item.properties["proj:epsg"] is None
    assert len(item.assets) == 1
