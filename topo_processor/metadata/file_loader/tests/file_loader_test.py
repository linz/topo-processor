import csv
import os
import tempfile
from typing import Dict

import pytest

from topo_processor.metadata.file_loader.file_loader import read_csv, read_gpkg


def test_read_csv() -> None:
    metadata_path = os.path.join(os.getcwd(), "test_data", "historical_aerial_photos_metadata.csv")
    metadata = read_csv(metadata_path, "raw_filename", "sufi")

    assert len(metadata) == 5
    assert list(metadata.keys()) == ["WRONG_PHOTO_TYPE", "MULTIPLE_ASSET", "CONTROL", "WRONG_SURVEY", "CONTROL_2"]


def test_read_gpkg() -> None:
    metadata_criteria: Dict[str, str] = {"raw_filename": "CONTROL"}
    metadata_path = os.path.join(os.getcwd(), "test_data", "historical_aerial_photos_metadata.gpkg")
    metadata = read_gpkg(metadata_path, metadata_criteria, "raw_filename")

    assert len(metadata) == 1
    assert list(metadata.keys()) == ["CONTROL"]


def test_error_on_wrong_file_name_csv() -> None:
    metadata_path = "./data/historical_aerial_photos_metadata.csv"

    with pytest.raises(Exception, match=r"^Cannot find "):
        read_csv(metadata_path, "raw_filename", "sufi")


def test_error_on_wrong_file_name_gpkg() -> None:
    metadata_path = "./data/historical_aerial_photos_metadata.gpkg"
    metadata_criteria: Dict[str, str] = {"raw_filename": "CONTROL"}

    with pytest.raises(Exception, match=r"^Cannot find "):
        read_gpkg(metadata_path, metadata_criteria, "raw_filename")


def test_error_on_duplicate_file_csv() -> None:
    temp_file = tempfile.NamedTemporaryFile()
    header = [
        "WKT",
        "sufi",
        "survey",
        "run",
        "photo_no",
        "alternate_survey_name",
        "camera",
        "camera_sequence_no",
        "nominal_focal_length",
        "altitude",
        "scale",
        "photocentre_lat",
        "photocentre_lon",
        "date",
        "film",
        "film_sequence_no",
        "photo_type",
        "format",
        "source",
        "physical_film_condition",
        "image_anomalies",
        "scanned",
        "raw_filename",
        "released_filename",
        "when_scanned",
        "photo_version",
    ]
    row = [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "WRONG_PHOTO_TYPE",
        "",
        "",
        "",
    ]
    with open(temp_file.name, "a", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerow(row)
        writer.writerow(row)

    with pytest.raises(Exception, match=r'Duplicate "WRONG_PHOTO_TYPE" found in "' + temp_file.name + '"'):
        read_csv(temp_file.name, "raw_filename", "sufi")


def test_error_on_duplicate_file_gpkg() -> None:

    metadata_criteria: Dict[str, str] = {"raw_filename": "CONTROL"}
    metadata_path = os.path.join(os.getcwd(), "test_data", "historical_aerial_photos_metadata_duplicate.gpkg")

    with pytest.raises(Exception, match=r'Duplicate "CONTROL" found in "' + metadata_path + '"'):
        read_gpkg(metadata_path, metadata_criteria, "raw_filename")


def test_read_csv_column_filter() -> None:
    metadata_path = os.path.join(os.getcwd(), "test_data", "historical_survey_footprint_metadata.csv")
    metadata = read_csv(metadata_path, "SURVEY", columns=["NAME"])

    assert len(metadata) == 4
    assert list(metadata.keys()) == ["SURVEY_1", "SURVEY_3", "SURVEY_2", "SURVEY_NO_NAME"]
    assert list(metadata.values()) == [{"NAME": "TE KUITI 1"}, {"NAME": "AUCKLAND 1"}, {"NAME": "WELLINGTON 2"}, {"NAME": ""}]


def test_read_csv_column_filter_gpkg() -> None:
    metadata_criteria: Dict[str, str] = {"SURVEY": "SURVEY_1"}
    metadata_path = os.path.join(os.getcwd(), "test_data", "historical_survey_footprint_metadata.gpkg")
    metadata = read_gpkg(metadata_path, metadata_criteria, "SURVEY", columns=["NAME"])

    assert len(metadata) == 1
    assert list(metadata.keys()) == ["SURVEY_1"]
    assert list(metadata.values()) == [{"NAME": "TE KUITI 1"}]