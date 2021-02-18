from topo_processor.factory.collection import Collection
from topo_processor.factory.data_type import DataType
from topo_processor.factory.item import Item

from .data_compressor_imagery_historic import DataCompressorImageryHistoric


def test_is_applicable():
    tiff_path = "test_path.tiff"
    collection = Collection("title", "description", "license", DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    compressor = DataCompressorImageryHistoric()
    assert compressor.is_applicable(item)


def test_is_not_applicable_wrong_file_extension():
    tiff_path = "test_path"
    collection = Collection("title", "description", "license", DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    compressor = DataCompressorImageryHistoric()
    assert not compressor.is_applicable(item)


def test_is_not_applicable_wrong_data_type():
    tiff_path = "test_path.tiff"
    collection = Collection("title", "description", "license", DataType.LidarPointCloud)
    item = Item(tiff_path, collection)
    compressor = DataCompressorImageryHistoric()
    assert not compressor.is_applicable(item)
