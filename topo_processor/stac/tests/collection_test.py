import pytest
import shapely.wkt

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


def test_polygon_union_empty():
    collection = Collection("fake_collection")
    assert collection.get_bounding_boxes() == [(0.0, 0.0, 0.0, 0.0)]


def test_polygon_union():
    collection = Collection("fake_collection")

    item_a = Item("id_1")
    collection.add_item(item_a)
    item_a.geometry_poly = shapely.wkt.loads("POLYGON ((1 2,1 4,3 4,3 2,1 2))")
    assert collection.get_bounding_boxes() == [(1.0, 2.0, 3.0, 4.0)]

    item_b = Item("id_2")
    collection.add_item(item_b)
    item_b.geometry_poly = shapely.wkt.loads("POLYGON ((5 6,5 8,7 8,7 6,5 6))")
    assert collection.get_bounding_boxes() == [(1.0, 2.0, 7.0, 8.0)]
