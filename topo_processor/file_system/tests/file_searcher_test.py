import os
from typing import List

import pytest

from topo_processor.file_system.file_searcher import get_file_path_from_survey


def test_get_file_path_from_survey() -> None:
    my_list: List[str] = []
    my_list.append("/tiffs/SURVEY_1/WRONG_PHOTO_TYPE.tif")
    my_list.append("/tiffs/SURVEY_1/MULTIPLE_ASSET.tif")
    my_list.append("/tiffs/SURVEY_1/CONTROL.tif")

    other_list: List[str] = []

    other_list = get_file_path_from_survey("test", "test", os.path.join(os.getcwd(), "test_data", "manifest.json"))
    print(my_list)
    print(other_list)

    assert my_list == other_list
