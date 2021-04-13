import os

import pytest

from topo_processor.util.checksum import multihash_as_hex


@pytest.mark.asyncio
async def test_mulithash_as_hex():
    path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "WRONG_SURVEY.tiff")
    assert await multihash_as_hex(path) == "1220d1bed69013d3dbcf4b1ef90016d77be83ad9b1759865ef5f9969ed540f902f53"

    path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "CONTROL.tiff")
    assert await multihash_as_hex(path) == "1220d3e42a62bb123eeeb96358f1e4ed46d20b1a329a4738dd643d27623ba8452957"

    path = os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1", "MULTIPLE_ASSET.tiff")
    assert await multihash_as_hex(path) == "1220d3e42a62bb123eeeb96358f1e4ed46d20b1a329a4738dd643d27623ba8452957"
