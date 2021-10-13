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


def test_camera_extension_added_if_empty_metadata():
    """Tests camera extension is still added if metadata is empty"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"camera_sequence_no": "", "nominal_focal_length": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_camera_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.camera.value in item.stac_extensions


def test_camera_metadata_added():
    """Tests camera metadata is added if one empty string"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"camera_sequence_no": "", "nominal_focal_length": "508"}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_camera_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.camera.value in item.stac_extensions
    assert item.properties["camera:nominal_focal_length"] == 508
    assert "camera:sequence_number" not in item.properties.keys()


def test_film_extension_added_if_empty_metadata():
    """Tests film extension is still added even if metadata is empty"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"film": "", "film_sequence_no": "", "physical_film_condition": "", "format": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_film_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.film.value in item.stac_extensions


def test_film_metadata_added():
    """Tests film metadata is is still added if one of them is an empty string"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"film": "123", "film_sequence_no": "234", "physical_film_condition": "", "format": "23 cm x 23 cm"}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_film_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.film.value in item.stac_extensions
    assert item.properties["film:id"] == "123"
    assert item.properties["film:negative_sequence"] == 234
    assert "film:physical_condition" not in item.properties.keys()
    assert item.properties["film:physical_size"] == "23 cm x 23 cm"


def test_aerial_photo_extension_added_if_empty_metadata():
    """Tests aerial-photo extension is still added if empty metadata"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"run": "", "altitude": "", "scale": "", "photo_no": "", "image_anomalies": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_aerial_photo_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.aerial_photo.value in item.stac_extensions
    assert "aerial-photo:run" not in item.properties.keys()
    assert "aerial-photo:altitude" not in item.properties.keys()
    assert "aerial-photo:scale" not in item.properties.keys()
    assert "aerial-photo:sequence_number" not in item.properties.keys()
    assert "aerial-photo:anomalies" not in item.properties.keys()


def test_aerial_photo_zero_altitude_scale():
    """Tests aerial-photo extension added and no metadata with zero values for altitude and scale"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"run": "", "altitude": "0", "scale": "0", "photo_no": "", "image_anomalies": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_aerial_photo_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.aerial_photo.value in item.stac_extensions
    assert "aerial-photo:altitude" not in item.properties.keys()
    assert "aerial-photo:scale" not in item.properties.keys()


def test_aerial_photo_metadata_added():
    """Test aerial-photo metadata is added if one is an empty string"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"run": "string", "altitude": "123", "scale": "123", "photo_no": "123", "image_anomalies": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_aerial_photo_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.aerial_photo.value in item.stac_extensions
    assert item.properties["aerial-photo:run"] == "string"
    assert item.properties["aerial-photo:altitude"] == 123
    assert item.properties["aerial-photo:scale"] == 123
    assert item.properties["aerial-photo:sequence_number"] == 123
    assert "aerial-photo:anomalies" not in item.properties.keys()


def test_scanning_metadata_not_added():
    """Tests scanning metadata is not added if two empty strings"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"source": "", "when_scanned": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_scanning_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.scanning.value not in item.stac_extensions
    assert "scan:is_original" not in item.properties.keys()
    assert "scan:scanned" not in item.properties.keys()


def test_not_add_scanning_is_original_metadata():
    """Tests scanning metadata is added if one empty string"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"source": "ORIGINAL", "when_scanned": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_scanning_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.scanning.value in item.stac_extensions
    assert item.properties["scan:is_original"] == True
    assert "scan:scanned" not in item.properties.keys()
