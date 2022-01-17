import os

from topo_processor.metadata.metadata_loaders.metadata_loader_tiff import MetadataLoaderTiff
from topo_processor.stac.asset import Asset
from topo_processor.stac.collection import Collection
from topo_processor.stac.item import Item
from topo_processor.stac.stac_extensions import StacExtensions


def test_load_metadata():
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = Asset(source_path)
    item = Item("item_id")
    item.add_asset(asset)
    item.collection = Collection("Collection")
    loader = MetadataLoaderTiff()
    assert loader.is_applicable(asset)

    loader.load_metadata(asset)
    assert item.properties["proj:epsg"] is None
    assert StacExtensions.projection.value in item.stac_extensions
    assert len(item.assets) == 1
    assert item.assets[0].properties["eo:bands"] == [{"name": "gray", "common_name": "pan"}]
    assert StacExtensions.eo.value in item.stac_extensions
