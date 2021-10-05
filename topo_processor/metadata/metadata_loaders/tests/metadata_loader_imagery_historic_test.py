import pytest

import topo_processor.stac as stac
from topo_processor.metadata.metadata_loaders.metadata_loader_imagery_historic import MetadataLoaderImageryHistoric


def test_is_applicable():
    source_path = "test_abc.tiff"
    asset = stac.Asset(source_path)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert metadata_loader_imagery_historic.is_applicable(asset)


def test_item_not_found_in_csv():
    source_path = "test_abc.tiff"
    asset = stac.Asset(source_path)
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.load_metadata(asset)
    error_msg = {
        "msg": "Asset not found in CSV file",
        "level": "error",
        "cause": "metadata.loader.imagery.historic",
        "error": None,
    }
    assert error_msg in asset.log


def test_camera_metadata_not_added():
    """Tests camera metadata is not added if two empty strings"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"camera_sequence_no": "", "nominal_focal_length": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_camera_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.camera.value not in item.stac_extensions
    assert "camera:nominal_focal_length" not in item.properties.keys()
    assert "camera:sequence_number" not in item.properties.keys()


def test_not_add_camera_sequence_number_metadata():
    """Tests camera metadata is added if one empty string"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"camera_sequence_no": "", "nominal_focal_length": "508"}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_camera_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.camera.value in item.stac_extensions
    assert item.properties["camera:nominal_focal_length"] == 508
    assert "camera:sequence_number" not in item.properties.keys()
