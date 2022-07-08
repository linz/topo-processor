import os
from typing import List

import pytest

from topo_processor.file_system.file_searcher import get_file_path_from_survey
from topo_processor.file_system.manifest import get_file_path_from_manifest, load_manifest


def test_get_file_path_from_manifest() -> None:
    assert_list: List[str] = []
    assert_list.append("/tiffs/SURVEY_1/CONTROL.tif")

    result_list: List[str] = []
    manifest = load_manifest(os.path.join(os.getcwd(), "test_data", "manifest.json"))
    result_list = get_file_path_from_manifest(manifest, ("control.tif", "control.tiff"))

    assert assert_list == result_list


def test_get_file_path_from_survey_csv() -> None:
    assert_list: List[str] = []
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/WRONG_PHOTO_TYPE.tif")
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/MULTIPLE_ASSET.tif")
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/CONTROL.tif")

    result_list: List[str] = get_file_path_from_survey(
        "SURVEY_1", os.path.join(os.getcwd(), "test_data", "manifest.json"), "test_data/historical_aerial_photos_metadata.csv"
    )

    assert result_list == assert_list


def test_get_file_path_from_survey_gpkg() -> None:
    assert_list: List[str] = []
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/WRONG_PHOTO_TYPE.tif")
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/MULTIPLE_ASSET.tif")
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/CONTROL.tif")

    result_list: List[str] = get_file_path_from_survey(
        "SURVEY_1", os.path.join(os.getcwd(), "test_data", "manifest.json"), "test_data/historical_aerial_photos_metadata.gpkg"
    )

    assert result_list == assert_list


def test_get_file_path_from_survey_duplicate_csv() -> None:
    assert_list: List[str] = []
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/WRONG_PHOTO_TYPE.tif")
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/MULTIPLE_ASSET.tif")
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/CONTROL.tif")

    with pytest.raises(Exception) as e:
        get_file_path_from_survey(
            "SURVEY_1",
            os.path.join(os.getcwd(), "test_data", "manifest_duplicate.json"),
            "test_data/historical_aerial_photos_metadata.csv",
        )
        assert "Duplicate files found" in str(e.value)


def test_get_file_path_from_survey_duplicate_gpkg() -> None:
    assert_list: List[str] = []
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/WRONG_PHOTO_TYPE.tif")
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/MULTIPLE_ASSET.tif")
    assert_list.append("s3://linz-historical-imagery-staging/tiffs/SURVEY_1/CONTROL.tif")

    with pytest.raises(Exception) as e:
        get_file_path_from_survey(
            "SURVEY_1",
            os.path.join(os.getcwd(), "test_data", "manifest_duplicate.json"),
            "test_data/historical_aerial_photos_metadata.gpkg",
        )
        assert "Duplicate files found" in str(e.value)
