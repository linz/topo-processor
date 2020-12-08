import asyncio
import os

from topo_processor.metadata.collection import Collection
from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.item import Item

from .metadata_loader_tiff import MetadataLoaderTiff


def test_add_metadata():
    tiff_path = os.path.join(os.getcwd(), "test_data", "tiffs", "CROWN_399_E_49.tiff")
    collection = Collection("title", "description", "license", DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    loader = MetadataLoaderTiff()
    assert loader.is_applicable(item)

    asyncio.run(loader.add_metadata(item))
    assert item.stac_item.properties["proj:epsg"] is None
    assert len(item.stac_item.assets) == 1
    assert item.stac_item.assets["image"].properties["linz:image_height"] == 9
