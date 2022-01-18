import os

import pytest

from topo_processor.stac.asset import Asset


def test_asset() -> None:
    """validate adding of extra field: file:checksum"""
    source_path = os.path.abspath(os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff"))
    asset = Asset(source_path)
    asset.href = "test_asset"
    checksum = asset.get_checksum()
    json_asset = asset.create_stac().to_dict()
    assert json_asset["file:checksum"] == checksum
