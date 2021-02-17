import asyncio

import pytest

from topo_processor.factory.collection import Collection
from topo_processor.factory.data_type import DataType
from topo_processor.factory.item import Item

from .metadata_loader_imagery_historic import MetadataLoaderImageryHistoric


def test_is_applicable():
    tiff_path = "test_path.tiff"
    collection = Collection(DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert metadata_loader_imagery_historic.is_applicable(item)


def test_is_not_applicable_wrong_file_extension():
    tiff_path = "test_path"
    collection = Collection(DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert not metadata_loader_imagery_historic.is_applicable(item)


def test_is_not_applicable_wrong_data_type():
    tiff_path = "test_path.tiff"
    collection = Collection(DataType.LidarPointCloud)
    item = Item(tiff_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert not metadata_loader_imagery_historic.is_applicable(item)


def test_item_not_found_in_csv():
    tiff_path = "test_path.tiff"
    collection = Collection(DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    with pytest.raises(Exception, match=r"test_path cannot be found in the csv."):
        asyncio.run(metadata_loader_imagery_historic.add_metadata(item))
