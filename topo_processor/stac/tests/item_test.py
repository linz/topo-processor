import pystac
import pytest

from topo_processor.stac import Asset, Collection, DataType, Item


def test_duplicate_asset():
    item = Item("fake/path/abc.tiff", DataType.ImageryHistoric, "fake/target", "fake_temp_dir")
    item.id = "item_id"
    item.collection = Collection("fake_title")
    item.add_asset(
        "cog1",
        Asset(
            key="image",
            path="fake_asset_path",
            content_type=pystac.MediaType.COG,
            file_ext=".tiff",
            needs_upload=True,
        ),
    )
    item.add_asset(
        "cog2",
        Asset(
            key="image",
            path="fake_asset_path",
            content_type=pystac.MediaType.COG,
            file_ext=".tiff",
            needs_upload=True,
        ),
    )
    item.assets["source"].needs_upload = False
    with pytest.raises(Exception, match=r"./fake_title/item_id.tiff already exists."):
        item.create_stac()
