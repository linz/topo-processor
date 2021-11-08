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


def test_scanning_extension_added_if_empty_metadata():
    """Tests scanning extension is still added if metadata is empty"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"source": "", "when_scanned": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_scanning_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.scanning.value in item.stac_extensions


def test_scanning_extension_invalid_values_date_wrong_format():
    """Tests scanning extension added with original strings for invalid values for source and when_scanned"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"source": "string", "when_scanned": "nzam_pilot"}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_scanning_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.scanning.value in item.stac_extensions
    assert item.properties["scan:is_original"] == "string"
    assert item.properties["scan:scanned"] == "nzam_pilot"


def test_scanning_metadata_added():
    """Tests scanning metadata is added if one empty string"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"source": "ORIGINAL", "when_scanned": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_scanning_metadata(item, asset_metadata=metadata)
    assert stac.StacExtensions.scanning.value in item.stac_extensions
    assert item.properties["scan:is_original"]
    assert "scan:scanned" not in item.properties.keys()


def test_add_datetime_property():
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"date": "1952-04-23T00:00:00.000"}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_datetime_property(item, asset_metadata=metadata)
    assert item.datetime is not None
    assert item.datetime.isoformat() == "1952-04-22T12:00:00+00:00"


def test_add_datetime_property_empty():
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"date": ""}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_datetime_property(item, asset_metadata=metadata)
    assert item.datetime is None


def test_add_datetime_property_not_date():
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"date": "toto"}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_datetime_property(item, asset_metadata=metadata)
    assert item.datetime is None


def test_spatial_metadata_empty():
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_spatial_extent(item, asset_metadata=metadata)
    assert item.geometry_poly is None


def test_spatial_metadata_polygon_empty():
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"WKT": "POLYGON EMPTY"}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_spatial_extent(item, asset_metadata=metadata)
    assert item.geometry_poly is None
    assert item.log[0]["msg"] == "Geometry is missing"
    assert item.log[0]["level"] == "warning"


def test_spatial_metadata_polygon_invalid():
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {"WKT": "POLYGON POLYGON ((177.168157744315 -38.7538525409217))"}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_spatial_extent(item, asset_metadata=metadata)
    assert item.geometry_poly is None
    assert item.log[0]["msg"] == "Geometry is invalid"
    assert item.log[0]["level"] == "error"


def test_spatial_metadata_polygon():
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {
        "WKT": "POLYGON ((177.168157744315 -38.7538525409217,177.23423558687 -38.7514276946524,177.237358655351 -38.8031681573174,177.17123348276 -38.8055953066942,177.168157744315 -38.7538525409217))"
    }
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_spatial_extent(item, asset_metadata=metadata)
    assert item.geometry_poly is not None
    assert item.geometry_poly.bounds == (177.16816, -38.8056, 177.23736, -38.75143)


def test_spatial_metadata_collection_polygon():
    item = stac.Item("test_abc.tiff")
    metadata = {
        "WKT": "POLYGON ((177.168157744315 -38.7538525409217,177.23423558687 -38.7514276946524,177.237358655351 -38.8031681573174,177.17123348276 -38.8055953066942,177.168157744315 -38.7538525409217))"
    }
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_spatial_extent(item, asset_metadata=metadata)

    assert item.geometry_poly is not None
    assert item.geometry_poly.bounds == (177.16816, -38.8056, 177.23736, -38.75143)


def test_centroid_metadata_added():
    """Tests centroid metadata is added correctly"""
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    metadata = {
        "photocentre_lat": "-41.28509",
        "photocentre_lon": "174.77442",
    }
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.add_centroid(item, asset_metadata=metadata)
    assert item.properties["proj:centroid"] == {"lat": -41.28509, "lon": 174.77442}
    assert stac.StacExtensions.projection.value in item.stac_extensions


def test_invalid_centroid_lat():
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    centroid = {
        "lat": 174.77442,
        "lon": 174.77442,
    }
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert not metadata_loader_imagery_historic.is_valid_centroid(item, centroid)
    assert (
        str(item.log[0]["error"]) == "stac field 'proj:centroid' has invalid lat value: 174.77442, instance: <class 'float'>"
    )


def test_invalid_centroid_lon():
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    centroid = {
        "lat": -41.28509,
        "lon": -190.0000,
    }
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert not metadata_loader_imagery_historic.is_valid_centroid(item, centroid)
    assert str(item.log[0]["error"]) == "stac field 'proj:centroid' has invalid lon value: -190.0, instance: <class 'float'>"


def test_invalid_centroid_string():
    source_path = "test_abc.tiff"
    item = stac.Item(source_path)
    centroid = {"lat": "-41.28509", "lon": "174.77442"}
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    assert not metadata_loader_imagery_historic.is_valid_centroid(item, centroid)
    assert str(item.log[0]["error"]) == "stac field 'proj:centroid' has invalid lat value: -41.28509, instance: <class 'str'>"


def test_mission_metadata_added_by_survey():
    """Tests mission metadata is added by survey value"""
    metadata = {
        "survey": "12345",
        "alternate_survey_name": "",
    }
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    title = metadata_loader_imagery_historic.get_title(metadata["survey"], metadata["alternate_survey_name"])
    assert title == "12345"


def test_mission_metadata_added_by_alternate_survey_name():
    """Tests mission metadata is added by alternate survey value"""
    metadata = {
        "survey": "0",
        "alternate_survey_name": "67890",
    }
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    title = metadata_loader_imagery_historic.get_title(metadata["survey"], metadata["alternate_survey_name"])
    assert title == "67890"


def test_mission_metadata_not_added():
    """Tests mission metadata is not added"""
    metadata = {
        "survey": "0",
        "alternate_survey_name": "",
    }
    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    title = metadata_loader_imagery_historic.get_title(metadata["survey"], metadata["alternate_survey_name"])
    assert title is None


def test_provider_added():
    source_path = "test_abc.tiff"
    asset = stac.Asset(source_path)
    metadata = {
        "WKT": "",
        "sufi": "",
        "survey": "SURVEY_1",
        "run": "",
        "photo_no": "",
        "alternate_survey_name": "",
        "camera": "",
        "camera_sequence_no": "",
        "nominal_focal_length": "",
        "altitude": "",
        "scale": "",
        "photocentre_lat": "",
        "photocentre_lon": "",
        "date": "",
        "film": "",
        "film_sequence_no": "",
        "photo_type": "",
        "format": "",
        "source": "",
        "physical_film_condition": "",
        "image_anomalies": "",
        "when_scanned": "",
    }

    metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
    metadata_loader_imagery_historic.populate_item(metadata, asset)
    collection = asset.item.collection.create_stac()
    assert len(collection.providers) == 2
    LINZ_provider = collection.providers[0]
    assert LINZ_provider.name == "Toitū Te Whenua LINZ"
    assert (
        LINZ_provider.description
        == "The New Zealand Government's lead agency for location and property information, Crown land and managing overseas investment."
    )
    assert (
        LINZ_provider.url
        == "https://www.linz.govt.nz/about-linz/what-were-doing/projects/crown-aerial-film-archive-historical-imagery-scanning-project"
    )
    assert LINZ_provider.roles == ["host", "licensor", "processor"]

    NZAM_provider = collection.providers[1]
    assert NZAM_provider.name == "NZ Aerial Mapping"
    assert NZAM_provider.description == "Aerial survey and geospatial services firm. Went into liquidation in 2014."
    assert NZAM_provider.roles == ["producer"]
