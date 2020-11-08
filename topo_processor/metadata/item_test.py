from topo_processor.metadata.collection import Collection
from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.item import Item


def test_output_filenames():

    tiff_path = "dir1/dir2/blahblahblah123.tiff"
    collection = Collection("title", "description", "license", DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    assert item.output_filename == "blahblahblah123.tiff.json"
