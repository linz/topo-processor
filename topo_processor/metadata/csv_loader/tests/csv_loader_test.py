import csv
import os
import tempfile

import pytest

from topo_processor.metadata.csv_loader.csv_loader import read_csv


def test_read_csv() -> None:
    metadata_path = os.path.join(os.getcwd(), "test_data", "historical_aerial_photos_metadata.csv")
    metadata = read_csv(metadata_path)

    assert len(metadata) == 5
    assert list(metadata.keys()) == ["WRONG_PHOTO_TYPE", "MULTIPLE_ASSET", "CONTROL", "WRONG_SURVEY", "CONTROL_2"]


def test_error_on_wrong_file_name() -> None:
    metadata_path = "./data/historical_aerial_photos_metadata.csv"

    with pytest.raises(Exception, match=r"^Cannot find "):
        read_csv(metadata_path)


def test_error_on_duplicate_file() -> None:
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

    with pytest.raises(Exception, match=r'Duplicate file "WRONG_PHOTO_TYPE" found in metadata csv'):
        read_csv(temp_file.name)