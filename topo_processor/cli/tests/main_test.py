import json
import asyncio
import os
import shutil
from tempfile import mkdtemp
from topo_processor.cli.main import main
import pytest

from topo_processor.cli.main import upload_to_local_disk
from topo_processor.stac import DataType, create_collection


@pytest.fixture(autouse=True)
def setup():
    """
    This function creates a temporary directory and deletes it after each test.
    See following link for details:
    https://docs.pytest.org/en/stable/fixture.html#yield-fixtures-recommended
    """
    source = os.path.join(os.getcwd(), "test_data", "tiffs", "C8054")
    datatype = "imagery.historic"
    target = mkdtemp()
    upload = False
    yield source, datatype, target, upload
    shutil.rmtree(target)


@pytest.mark.asyncio
async def test_upload_to_local(setup):
    source, datatype, target, upload = setup
    source_dir = os.path.abspath(source)
    data_type = DataType(datatype)
    collection = await create_collection(source_dir, data_type)
    await upload_to_local_disk(collection, target)
    shutil.rmtree(collection.temp_dir)

    assert os.path.isfile(os.path.join(target, "C8054", "29659.json"))
    assert os.path.isfile(os.path.join(target, "C8054", "29659.tiff"))
    assert os.path.isfile(os.path.join(target, "C8054", "collection.json"))

    with open(os.path.join(target, "C8054", "29659.json")) as item_json_file:
        item_metadata = json.load(item_json_file)

    assert item_metadata["properties"]["linz:survey"] == "C8054"
    assert item_metadata["properties"]["linz:sufi"] == "29659"
    assert item_metadata["id"] == item_metadata["properties"]["linz:sufi"]
    assert (
        item_metadata["assets"]["image"]["file:checksum"]
        == "122083318d91bfb2a04a82b381e2024d925a5ab3deababa0058dcb1b19ae4e805c9a"
    )
    assert (item_metadata["assets"]["image"]["href"]) == "C8054/29659.tiff"
