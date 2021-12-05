import os

from topo_processor import stac
from topo_processor.metadata.metadata_loaders.metadata_loader_tiff import MetadataLoaderTiff


def test_load_metadata():
    source_path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    asset = stac.Asset(source_path)
    item = stac.Item("item_id")
    item.add_asset(asset)
    item.collection = stac.Collection("Collection")
    loader = MetadataLoaderTiff()
    assert loader.is_applicable(asset)

    loader.load_metadata(asset)
    assert item.properties["proj:epsg"] is None
    assert stac.StacExtensions.projection.value in item.stac_extensions
    assert len(item.assets) == 1
    assert item.assets[0].properties["eo:bands"] == [{"name": "gray", "common_name": "pan"}]
    assert stac.StacExtensions.eo.value in item.stac_extensions
