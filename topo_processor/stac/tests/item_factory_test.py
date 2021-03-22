import pytest

from topo_processor.stac import DataType, Item, item_factory


def test_duplicate_item():
    item_a = Item("fake/path/a.tiff", DataType.ImageryHistoric, "fake/target", "fake_temp_dir")
    item_a.id = "same_id"
    item_a.parent = "fake_parent"
    item_b = Item("fake/path/b.tiff", DataType.ImageryHistoric, "fake/target", "fake_temp_dir")
    item_b.id = "same_id"
    item_b.parent = "fake_parent"
    with pytest.raises(Exception, match=r"Duplicate Items: fake/path/b.tiff"):

        for item in [item_a, item_b]:
            item_factory.link_collection_item(item)
