import os

import pytest

from topo_processor.stac import Asset


def test_asset():
    """validate adding of extra field: file:checksum"""
    source_path = os.path.abspath(os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff"))
    asset = Asset(source_path)
    asset.href = "test_asset"
    checksum = asset.get_checksum()
    json_asset = asset.create_stac().to_dict()
    assert json_asset["file:checksum"] == checksum


def test_asset_key_visual():
    """validate value of asset object key for a tiff"""
    source_path = os.path.abspath(os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff"))
    asset = Asset(source_path)
    asset.content_type = "image/tiff; application=geotiff; profile=cloud-optimized"
    key = asset.get_key()
    assert key == "visual"


def test_asset_key_no_content_type():
    """validate value of asset object key for an unknown content type with a file extension"""
    source_path = os.path.abspath(os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff"))
    asset = Asset(source_path)
    asset.content_type = ""
    key = asset.get_key()
    assert key == ".tiff"


def test_asset_key_no_content_type_no_file_ext(mocker):
    """validate value of asset object key for an unknown content type with no file extension"""
    source_path = os.path.abspath(os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff"))
    asset = Asset(source_path)
    asset.content_type = ""
    mocker.patch("topo_processor.stac.asset.Asset.file_ext", return_value="")
    key = asset.get_key()
    assert key == asset.get_checksum()
