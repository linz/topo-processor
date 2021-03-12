import json
import os
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.cli.main import upload_to_local_disk
from topo_processor.stac import DataType, create_collection


@pytest.mark.asyncio
@pytest.fixture(autouse=True)
async def setup():
    """
    This function creates a temporary directory and deletes it after each test.
    See following link for details:
    https://docs.pytest.org/en/stable/fixture.html#yield-fixtures-recommended
    """
    source = os.path.join(os.getcwd(), "test_data", "tiffs", "C8054")
    datatype = "imagery.historic"
    collection = await create_collection(source, DataType(datatype))
    target = mkdtemp()
    yield collection, target
    shutil.rmtree(target)
    shutil.rmtree(collection.temp_dir)


@pytest.mark.asyncio
async def test_local_save_paths(setup):
    collection, target = setup

    await upload_to_local_disk(collection, target)

    assert os.path.isfile(os.path.join(target, "C8054", "29659.json"))
    assert os.path.isfile(os.path.join(target, "C8054", "29659.lzw.cog.tiff"))
    assert os.path.isfile(os.path.join(target, "C8054", "collection.json"))


@pytest.mark.asyncio
async def test_item_contents(setup):
    collection, target = setup

    await upload_to_local_disk(collection, target)

    with open(os.path.join(target, "C8054", "29659.json")) as item_json_file:
        item_metadata = json.load(item_json_file)

    assert item_metadata["properties"]["linz:survey"] == "C8054"
    assert item_metadata["properties"]["linz:sufi"] == "29659"
    assert item_metadata["id"] == item_metadata["properties"]["linz:sufi"]
    assert (
        item_metadata["assets"]["cog"]["file:checksum"]
        == "122083318d91bfb2a04a82b381e2024d925a5ab3deababa0058dcb1b19ae4e805c9a"
    )
    assert (item_metadata["assets"]["cog"]["href"]) == "C8054/29659.lzw.cog.tiff"
