import os

import pytest

from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.lds_cache.lds_cache import filter_metadata, get_metadata


def test_filter_metadata() -> None:
    metadata = {
        "file_a": {"survey": "survey_1", "camera": "camera_a", "raw_filename": "file_a"},
        "file_b": {"survey": "survey_3", "camera": "camera_b", "raw_filename": "file_b"},
        "file_c": {"survey": "survey_1", "camera": "camera_b", "raw_filename": "file_c"},
    }

    criteria = {"survey": "survey_1"}

    metadata_filtered = {
        "file_a": {"survey": "survey_1", "camera": "camera_a", "raw_filename": "file_a"},
        "file_c": {"survey": "survey_1", "camera": "camera_b", "raw_filename": "file_c"},
    }

    result = filter_metadata(metadata, criteria)

    assert metadata_filtered == result


def test_filter_metadata_asset() -> None:
    metadata = {
        "file_a": {"survey": "survey_1", "camera": "camera_a", "raw_filename": "file_a"},
        "file_b": {"survey": "survey_3", "camera": "camera_b", "raw_filename": "file_b"},
        "file_c": {"survey": "survey_1", "camera": "camera_b", "raw_filename": "file_c"},
    }

    criteria = {"raw_filename": "file_a"}

    metadata_filtered = {
        "file_a": {"survey": "survey_1", "camera": "camera_a", "raw_filename": "file_a"},
    }

    result = filter_metadata(metadata, criteria)

    assert metadata_filtered == result


def test_get_metadata_csv() -> None:
    metadata = {
        "WRONG_SURVEY": {
            "WKT": "POLYGON ((170.540066918452 -45.8023553587759,170.559584102313 -45.8027545634288,170.559139228268 -45.8134376154951,170.539618358047 -45.8130383744392,170.540066918452 -45.8023553587759))",
            "sufi": "72352",
            "survey": "SURVEY_3",
            "run": "E",
            "photo_no": "48",
            "alternate_survey_name": "",
            "camera": "EAGLE IV",
            "camera_sequence_no": "89556",
            "nominal_focal_length": "508",
            "altitude": "11000",
            "scale": "6600",
            "photocentre_lat": "-45.8079",
            "photocentre_lon": "170.5496",
            "date": "1952-04-23T00:00:00.000",
            "film": "731",
            "film_sequence_no": "114",
            "photo_type": "B&W",
            "format": "18cm x 23cm",
            "source": "ORIGINAL ",
            "physical_film_condition": "",
            "image_anomalies": "",
            "scanned": "Y",
            "raw_filename": "WRONG_SURVEY",
            "released_filename": "CROWN_731_114",
            "when_scanned": "2020/Q4",
            "photo_version": "1",
        }
    }
    metadata_path = os.path.abspath(os.path.join(os.getcwd(), "test_data", "historical_aerial_photos_metadata.csv"))
    criteria = {"survey": "SURVEY_3"}
    result = get_metadata(DataType.IMAGERY_HISTORIC, criteria, metadata_path)

    assert metadata == result


def test_get_metadata_gpkg() -> None:

    metadata = {
        "WRONG_SURVEY": {
            "fid": "4",
            "geom": "b'GP\\x00\\x03\\x00\\x00\\x00\\x00B\\x04\\xb8\\x8dDQe@xY\\xeb\\x1c\\xe8Qe@\\x9f\\xf1I\\xb9\\x1e\\xe8F\\xc0>\\xdb\\x94\\x94\\xb3\\xe6F\\xc0\\x01\\x03\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x05\\x00\\x00\\x00\\xe4\\x0ck:HQe@>\\xdb\\x94\\x94\\xb3\\xe6F\\xc0xY\\xeb\\x1c\\xe8Qe@\\x1bRZ\\xa9\\xc0\\xe6F\\xc0Lj\\xf3w\\xe4Qe@\\x9f\\xf1I\\xb9\\x1e\\xe8F\\xc0B\\x04\\xb8\\x8dDQe@\\x00N6\\xa4\\x11\\xe8F\\xc0\\xe4\\x0ck:HQe@>\\xdb\\x94\\x94\\xb3\\xe6F\\xc0'",
            "WKT": "POLYGON ((170.540066918452 -45.8023553587759,170.559584102313 -45.8027545634288,170.559139228268 -45.8134376154951,170.539618358047 -45.8130383744392,170.540066918452 -45.8023553587759))",
            "sufi": "72352",
            "survey": "SURVEY_3",
            "run": "E",
            "photo_no": "48",
            "alternate_survey_name": "",
            "camera": "EAGLE IV",
            "camera_sequence_no": "89556",
            "nominal_focal_length": "508",
            "altitude": "11000",
            "scale": "6600",
            "photocentre_lat": "-45.8079",
            "photocentre_lon": "170.5496",
            "date": "1952-04-23T00:00:00.000",
            "film": "731",
            "film_sequence_no": "114",
            "photo_type": "B&W",
            "format": "18cm x 23cm",
            "source": "ORIGINAL ",
            "physical_film_condition": "",
            "image_anomalies": "",
            "scanned": "Y",
            "raw_filename": "WRONG_SURVEY",
            "released_filename": "CROWN_731_114",
            "when_scanned": "2020/Q4",
            "photo_version": "1",
        }
    }

    metadata_path = os.path.abspath(os.path.join(os.getcwd(), "test_data", "historical_aerial_photos_metadata.gpkg"))
    criteria = {"survey": "SURVEY_3"}
    result = get_metadata(DataType.IMAGERY_HISTORIC, criteria, metadata_path)

    assert metadata == result
