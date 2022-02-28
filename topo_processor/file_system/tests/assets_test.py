import os

import pytest

from topo_processor.file_system.assets import _get_assets_from_directory
from topo_processor.metadata.data_type import DataType


def test_get_assets_from_directory() -> None:
    source = os.path.abspath(os.path.join(os.getcwd(), "test_data", "tiffs"))
    assets_list = _get_assets_from_directory(source, DataType.IMAGERY_HISTORIC)

    assert len(assets_list) == 5
