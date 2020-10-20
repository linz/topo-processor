from topo_processor.metadata.collection import Collection
from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.item import Item

from .metadata_loader_imagery_historic import MetadataLoaderImageryHistoric


def test_is_applicable():
    tiff_path = "test_path.tiff"
    collection = Collection("title", "description", "license", DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert metadata_loader_imagery_historic.is_applicable(item)


def test_is_not_applicable_wrong_file_extension():
    tiff_path = "test_path"
    collection = Collection("title", "description", "license", DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert not metadata_loader_imagery_historic.is_applicable(item)


def test_is_not_applicable_wrong_data_type():
    tiff_path = "test_path.tiff"
    collection = Collection("title", "description", "license", DataType.LidarPointCloud)
    item = Item(tiff_path, collection)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert not metadata_loader_imagery_historic.is_applicable(item)
