from datetime import datetime

import pystac.validation
import pytest
import shapely.wkt
from pystac.errors import STACValidationError

from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.metadata_loaders.metadata_loader_imagery_historic import MetadataLoaderImageryHistoric
from topo_processor.stac.asset import Asset
from topo_processor.stac.collection import Collection
from topo_processor.stac.item import Item
from topo_processor.stac.iter_errors_validator import IterErrorsValidator
from topo_processor.stac.linz_provider import LinzProviders
from topo_processor.stac.stac_extensions import StacExtensions


def test_duplicate_item() -> None:
    """Same Id different data"""
    item_a = Item("same_id")
    item_b = Item("same_id")
    item_b.properties = {"fake_metadata": "fake_metadata"}
    collection = Collection("fake_collection")
    collection.add_item(item_a)
    with pytest.raises(Exception, match=r"Remapping of item id in collection='fake_collection' item='same_id'"):
        collection.add_item(item_b)


def test_duplicate_item_two() -> None:
    """Identical items"""
    item_a = Item("same_id")
    item_b = Item("same_id")
    collection = Collection("fake_collection")
    collection.add_item(item_a)
    with pytest.raises(Exception, match=r"Remapping of item id in collection='fake_collection' item='same_id'"):
        collection.add_item(item_b)


def test_create_stac() -> None:
    collection = Collection("fake_collection")
    collection.description = "fake_collection_description"
    collection.license = "fake_license"
    json_collection = collection.create_stac().to_dict()
    assert json_collection["type"] == "Collection"
    assert json_collection["stac_version"] == "1.0.0"


def test_polygon_union_empty() -> None:
    collection = Collection("fake_collection")
    assert collection.get_bounding_boxes() == [[0.0, 0.0, 0.0, 0.0]]


def test_polygon_union() -> None:
    collection = Collection("fake_collection")

    item_a = Item("id_1")
    collection.add_item(item_a)
    item_a.geometry_poly = shapely.wkt.loads("POLYGON ((1 2,1 4,3 4,3 2,1 2))")
    assert collection.get_bounding_boxes() == [[1.0, 2.0, 3.0, 4.0]]

    item_b = Item("id_2")
    collection.add_item(item_b)
    item_b.geometry_poly = shapely.wkt.loads("POLYGON ((5 6,5 8,7 8,7 6,5 6))")
    assert collection.get_bounding_boxes() == [[1.0, 2.0, 7.0, 8.0]]


def test_get_temporal_extent() -> None:
    collection = Collection("fake_collection")
    datetime_earliest = datetime.strptime("1918-11-11", "%Y-%m-%d")
    datetime_mid = datetime.strptime("1945-05-08", "%Y-%m-%d")
    datetime_latest = datetime.strptime("1989-11-09", "%Y-%m-%d")

    item_x = Item("id_0")
    item_x.datetime = None
    collection.add_item(item_x)

    item_a = Item("id_1")
    item_a.datetime = datetime_latest
    collection.add_item(item_a)

    item_b = Item("id_2")
    item_b.datetime = datetime_earliest
    collection.add_item(item_b)

    item_c = Item("id_3")
    item_c.datetime = None
    collection.add_item(item_c)

    item_d = Item("id_4")
    item_d.datetime = datetime_mid
    collection.add_item(item_d)

    assert collection.get_temporal_extent() == [datetime_earliest, datetime_latest]


def test_get_linz_asset_summaries() -> None:
    collection = Collection("fake_title")
    item = Item("item_id")
    collection.add_item(item)

    cog_1 = Asset("testa")
    cog_1.properties["created"] = "1999-01-01T00:00:00Z"
    cog_1.properties["updated"] = "1999-01-01T00:00:00Z"
    cog_1.properties["processing:software"] = {"Topo Processor": "v0.1.0"}
    item.add_asset(cog_1)

    cog_2 = Asset("testb")
    cog_2.properties["created"] = "2010-01-01T00:00:00Z"
    cog_2.properties["updated"] = "2010-03-01T00:00:00Z"
    cog_2.properties["processing:software"] = {"Topo Processor": "v0.1.0"}
    item.add_asset(cog_2)

    assert collection.get_linz_asset_summaries() == {
        "processing:software": [{"Topo Processor": "v0.1.0"}],
        "created": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-01-01T00:00:00Z"},
        "updated": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-03-01T00:00:00Z"},
    }


def test_get_linz_multiple_processing_software_asset_summaries() -> None:
    collection = Collection("fake_title")
    item = Item("item_id")
    collection.add_item(item)

    cog_1 = Asset("testa")
    cog_1.properties["created"] = "1999-01-01T00:00:00Z"
    cog_1.properties["updated"] = "1999-01-01T00:00:00Z"
    cog_1.properties["processing:software"] = {"Topo Processor": "v0.1.0"}
    item.add_asset(cog_1)

    cog_2 = Asset("testb")
    cog_2.properties["created"] = "2010-01-01T00:00:00Z"
    cog_2.properties["updated"] = "2010-03-01T00:00:00Z"
    cog_2.properties["processing:software"] = {"Topo Processor": "v0.3.0"}
    item.add_asset(cog_2)

    assert collection.get_linz_asset_summaries() == {
        "processing:software": [{"Topo Processor": "v0.1.0"}, {"Topo Processor": "v0.3.0"}],
        "created": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-01-01T00:00:00Z"},
        "updated": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-03-01T00:00:00Z"},
    }


def test_get_linz_multiple__identical_processing_software_asset_summaries() -> None:
    collection = Collection("fake_title")
    item = Item("item_id")
    collection.add_item(item)

    cog_1 = Asset("testa")
    cog_1.properties["created"] = "1999-01-01T00:00:00Z"
    cog_1.properties["updated"] = "1999-01-01T00:00:00Z"
    cog_1.properties["processing:software"] = {"Topo Processor": "v0.3.0"}
    item.add_asset(cog_1)

    cog_2 = Asset("testb")
    cog_2.properties["created"] = "2010-01-01T00:00:00Z"
    cog_2.properties["updated"] = "2010-03-01T00:00:00Z"
    cog_2.properties["processing:software"] = {"Topo Processor": "v0.3.0"}
    item.add_asset(cog_2)

    assert collection.get_linz_asset_summaries() == {
        "processing:software": [{"Topo Processor": "v0.3.0"}],
        "created": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-01-01T00:00:00Z"},
        "updated": {"minimum": "1999-01-01T00:00:00Z", "maximum": "2010-03-01T00:00:00Z"},
    }


def test_single_geospatial_types() -> None:
    """Single photo_type"""

    collection = Collection("fake_collection")

    item_a = Item("id_0")
    item_a.linz_geospatial_type = "color image"
    collection.add_item(item_a)

    item_b = Item("id_1")
    item_b.linz_geospatial_type = "color image"
    collection.add_item(item_b)

    assert collection.get_linz_geospatial_type() == "color image"


def test_multiple_geospatial_types() -> None:
    """Multiple photo_type"""

    collection = Collection("fake_collection")

    item_a = Item("id_0")
    item_a.linz_geospatial_type = "black and white image"
    collection.add_item(item_a)

    item_b = Item("id_1")
    item_b.linz_geospatial_type = "black and white infrared image"
    collection.add_item(item_b)

    assert collection.get_linz_geospatial_type() == "invalid geospatial type"


def test_empty_geospatial_types() -> None:
    """Empty photo_type"""

    collection = Collection("fake_collection")

    item_a = Item("id_0")
    item_a.linz_geospatial_type = ""
    collection.add_item(item_a)

    item_b = Item("id_1")
    item_b.linz_geospatial_type = ""
    collection.add_item(item_b)

    assert collection.get_linz_geospatial_type() == "invalid geospatial type"


def test_historical_imagery_collection_description() -> None:
    "Correct Description"
    collection = Collection("fake_collection")
    collection.license = "CC-BY-4.0"

    item = Item("id")
    item.linz_geospatial_type = "black and white image"
    collection.add_item(item)

    collection.summaries.add("film:physical_size", ["120 x 120"])
    collection.description = "This aerial photographic survey was digitised from {} {} negatives in the Crown collection of the Crown Aerial Film Archive."

    stac_collection = collection.create_stac()
    collection.update_description(stac_collection, DataType("imagery.historic"))
    assert (
        collection.description
        == "This aerial photographic survey was digitised from black and white image 120 x 120 negatives in the Crown collection of the Crown Aerial Film Archive."
    )


def test_historical_imagery_collection_empty_description() -> None:
    "Empty Description"
    collection = Collection("fake_collection")
    collection.license = "CC-BY-4.0"

    item = Item("id")
    item.linz_geospatial_type = "black and white image"
    collection.add_item(item)

    collection.summaries.add("film:physical_size", ["120 x 120"])

    stac_collection = collection.create_stac()
    collection.update_description(stac_collection, DataType("imagery.aerial"))
    assert collection.description == ""


def test_validate_collection_with_summaries_iter_validator(setup: str) -> None:
    target = setup
    collection = Collection("AUCKLAND 1")
    collection.description = "fake_description"
    collection.license = "face_license"
    collection.survey = "SURVEY_1"
    collection.add_linz_provider(LinzProviders.LTTW.value)
    collection.add_linz_provider(LinzProviders.LMPP.value)
    collection.extra_fields.update(
        {
            "linz:lifecycle": "completed",
            "linz:history": "LINZ and its predecessors, Lands & Survey and Department of Survey and Land Information (DOSLI), commissioned aerial photography for the Crown between 1936 and 2008.",
            "quality:description": "The spatial extents provided are only an approximate coverage for the ungeoreferenced aerial photographs.",
        }
    )
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
    stac_item_1 = item_1.create_stac()

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
    stac_item_2 = item_2.create_stac()

    collection.add_extension(StacExtensions.historical_imagery.value)
    collection.add_extension(StacExtensions.linz.value)
    collection.add_extension(StacExtensions.quality.value)
    collection.add_extension(StacExtensions.aerial_photo.value)
    collection.add_extension(StacExtensions.camera.value)
    collection.add_extension(StacExtensions.film.value)
    collection.add_extension(StacExtensions.scanning.value)
    collection.add_extension(StacExtensions.eo.value)
    collection.add_extension(StacExtensions.file.value)
    collection.add_extension(StacExtensions.projection.value)
    collection.add_extension(StacExtensions.version.value)

    pystac_collection = collection.create_stac()

    # validator = MetadataValidatorStac()
    pystac_collection = item_1.collection.create_stac()
    pystac_collection.add_item(stac_item_1)
    pystac_collection.add_item(stac_item_2)
    collection.generate_summaries(pystac_collection)

    assert isinstance(pystac.validation.RegisteredValidator.get_validator(), IterErrorsValidator)
    with pytest.raises(Exception) as e:
        collection.validate_pystac_collection(pystac_collection)
    assert "summaries" not in str(e.value)
    assert "linz/schema.json" in str(e.value)
    assert "film/schema.json" in str(e.value)
    assert "aerial-photo:run" in str(e.value)
    assert "aerial-photo:sequence_number" in str(e.value)
