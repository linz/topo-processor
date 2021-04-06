import pytest

from topo_processor.metadata.metadata_loaders.metadata_loader_imagery_historic import MetadataLoaderImageryHistoric
from topo_processor.stac import Asset


def test_is_applicable():
    source_path = "test_abc.tiff"
    asset = Asset(source_path)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert metadata_loader_imagery_historic.is_applicable(asset)


@pytest.mark.asyncio
async def test_item_not_found_in_csv():
    source_path = "test_abc.tiff"
    asset = Asset(source_path)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    await metadata_loader_imagery_historic.load_metadata(asset)
    error_msg = {
        "msg": "Asset not found in CSV file",
        "level": "error",
        "cause": "metadata.loader.imagery.historic",
        "error": None,
    }
    assert error_msg in asset.log
