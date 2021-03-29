import pytest

from topo_processor.stac import Asset, Collection, Item


def test_duplicate_asset():
    item = Item("item_id")
    item.collection = Collection("fake_title")

    cog_1 = Asset("fake_asset_path")
    cog_1.target = "fake_target.tiff"
    item.add_asset(cog_1)

    cog_2 = Asset("fake_asset_path2")
    cog_2.target = "fake_target.tiff"
    item.add_asset(cog_2)

    with pytest.raises(Exception, match=r"./fake_title/item_id.tiff already exists."):
        item.create_stac()
