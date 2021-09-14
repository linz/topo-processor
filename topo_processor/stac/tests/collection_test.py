import pytest

from topo_processor.stac import Collection, Item


def test_duplicate_item():
    """Same Id different data"""
    item_a = Item("same_id")
    item_b = Item("same_id")
    item_b.properties = {"fake_metadata": "fake_metadata"}
    collection = Collection("fake_collection")
    collection.add_item(item_a)
    with pytest.raises(Exception, match=r"Remapping of item id in collection='fake_collection' item='same_id'"):
        collection.add_item(item_b)


def test_duplicate_item_two():
    """Identical items"""
    item_a = Item("same_id")
    item_b = Item("same_id")
    collection = Collection("fake_collection")
    collection.add_item(item_a)
    with pytest.raises(Exception, match=r"Remapping of item id in collection='fake_collection' item='same_id'"):
        collection.add_item(item_b)


def test_create_stac():
    collection = Collection("fake_collection")
    collection.description = "fake_collection_description"
    collection.license = "fake_license"
    json_collection = collection.create_stac().to_dict()
    assert json_collection["type"] == "Collection"
    assert json_collection["stac_version"] == "1.0.0"
