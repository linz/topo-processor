import os

import pytest

from topo_processor.file_system.get_fs import get_fs
from topo_processor.file_system.transfer import transfer_file


def test_transfer_local(setup: str) -> None:
    dest_path = f"{setup}/test.tiff"
    input_path = os.path.join(os.getcwd(), "test_data/tiffs/SURVEY_1/CONTROL.tiff")
    transfer_file(input_path, "fakechecksum", "image/tiff", dest_path)
    assert get_fs(input_path).info(input_path)["size"] == get_fs(dest_path).info(dest_path)["size"]
