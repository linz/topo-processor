import json
import os
from datetime import datetime

import pytest

from topo_processor.metadata.metadata_loaders.metadata_loader_imagery_historic import MetadataLoaderImageryHistoric
from topo_processor.stac.asset import Asset
from topo_processor.stac.asset_key import AssetKey
from topo_processor.stac.collection import Collection
from topo_processor.stac.item import Item
from topo_processor.util.transfer_collection import transfer_collection


def test_fail_on_duplicate_assets(setup: str) -> None:
    target = setup
    collection = Collection("fake_title")
    collection.survey = "survey_id"
    collection.description = "fake_description"
    collection.license = "fake_license"
    item = Item("item_id")
    item.datetime = datetime.now()
    item.linz_geospatial_type = "black and white image"
    collection.add_item(item)
    item.collection = collection

    cog_1 = Asset("./test_data/tiffs/SURVEY_1/CONTROL.tiff")
    cog_1.target = "fake_title/fake_target.tiff"
    cog_1.key_name = AssetKey.Visual
    item.add_asset(cog_1)

    cog_2 = Asset("test_data/tiffs/SURVEY_1/MULTIPLE_ASSET.tiff")
    cog_2.target = "fake_title/fake_target.tiff"
    cog_2.key_name = AssetKey.Visual
    item.add_asset(cog_2)

    with pytest.raises(Exception, match=r"./item_id.tiff already exists."):
        transfer_collection(item.collection, target)


def test_asset_key_not_in_list(setup: str) -> None:
    target = setup
    collection = Collection("fake_title")
    collection.survey = "survey_id"
    collection.description = "fake_description"
    collection.license = "fake_license"
    item = Item("item_id")
    item.datetime = datetime.now()
    item.linz_geospatial_type = "black and white image"
    collection.add_item(item)
    item.collection = collection

    test_asset = Asset("./test_data/tiffs/SURVEY_1/CONTROL.tiff")
    test_asset.target = "fake_title/fake_target.tiff"
    test_asset.key_name = None
    item.add_asset(test_asset)

    with pytest.raises(Exception, match=r"No asset key set for asset ./item_id.tiff"):
        transfer_collection(item.collection, target)


def test_generate_summaries(setup: str) -> None:
    target = setup
    collection = Collection("AUCKLAND 1")
    collection.description = "fake_description"
    collection.license = "face_license"
    collection.survey = "SURVEY_1"
    test_geom = {
        "WKT": "POLYGON ((177.168157744315 -38.7538525409217,"
        "177.23423558687 -38.7514276946524,"
        "177.237358655351 -38.8031681573174,"
        "177.17123348276 -38.8055953066942,"
        "177.168157744315 -38.7538525409217))"
    }
    test_datetime = datetime.strptime("1918-11-11", "%Y-%m-%d")

    item_1 = Item("item_1_id")
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_spatial_extent(item_1, asset_metadata=test_geom)
    item_1.datetime = test_datetime
    item_1.properties = {
        "mission": "SURVEY_1",
        "proj:centroid": {"lat": -45.8079, "lon": 170.5548},
        "camera:sequence_number": 89555,
        "film:id": "731",
        "aerial-photo:scale": 6600,
        "scan:scanned": "2014-06-30T12:00:00Z",
        "proj:epsg": "null",
    }
    collection.add_item(item_1)
    item_1.collection = collection

    item_2 = Item("item_2_id")
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_spatial_extent(item_2, asset_metadata=test_geom)
    item_2.datetime = test_datetime
    item_2.properties = {
        "mission": "SURVEY_1",
        "proj:centroid": {"lat": -45.8079, "lon": 170.5599},
        "camera:sequence_number": 89554,
        "film:id": "731",
        "aerial-photo:scale": 5600,
        "scan:scanned": "2019-12-31T11:00:00Z",
        "proj:epsg": "null",
    }
    collection.add_item(item_2)
    item_2.collection = collection

    transfer_collection(item_1.collection, target)

    with open(os.path.join(target, "SURVEY_1", "collection.json")) as collection_json_file:
        collection_metadata = json.load(collection_json_file)
        assert collection_metadata["summaries"]["mission"] == ["SURVEY_1"]
        assert collection_metadata["summaries"]["film:id"] == ["731"]
        assert collection_metadata["summaries"]["proj:epsg"] == ["null"]
        assert collection_metadata["summaries"]["aerial-photo:scale"] == {"minimum": 5600, "maximum": 6600}
        assert collection_metadata["summaries"]["scan:scanned"] == {
            "minimum": "2014-06-30T12:00:00Z",
            "maximum": "2019-12-31T11:00:00Z",
        }
        assert collection_metadata["summaries"]["camera:sequence_number"] == {"minimum": 89554, "maximum": 89555}
        assert "proj:centroid" not in collection_metadata["summaries"].keys()
