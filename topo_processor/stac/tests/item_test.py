import pystac
import pytest

from topo_processor.stac.asset import Asset
from topo_processor.stac.collection import Collection
from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item


def test_duplicate_asset():
    collection = Collection(DataType.ImageryHistoric, "fake_temp_dir")
    collection.title = "collection_title"
    item = Item("fake/path/abc.tiff", collection)
    item.id = "item_id"
    item.add_asset(
        "cog",
        Asset(
            key="image",
            path="fake_asset_path",
            content_type=pystac.MediaType.COG,
            file_ext=".tiff",
            needs_upload=True,
        ),
    )
    item.add_asset(
        "cog",
        Asset(
            key="image",
            path="fake_asset_path",
            content_type=pystac.MediaType.COG,
            file_ext=".tiff",
            needs_upload=True,
        ),
    )
    with pytest.raises(Exception, match=r"./collection_title/item_id.tiff already exists."):
        item.create_stac()
