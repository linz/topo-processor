import json
import os
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.cli.main import upload_to_local_disk
from topo_processor.stac import DataType, collection_store, create_items


@pytest.fixture(autouse=True)
def setup():
    """
    This function creates a temporary directory and deletes it after each test.
    See following link for details:
    https://docs.pytest.org/en/stable/fixture.html#yield-fixtures-recommended
    """
    datatype = DataType.ImageryHistoric
    target = mkdtemp()
    temp_dir = mkdtemp()
    yield datatype, target, temp_dir
    shutil.rmtree(target)
    shutil.rmtree(temp_dir)


@pytest.mark.asyncio
async def test_upload_local(setup):
    source_dir = os.path.abspath(os.path.join(os.getcwd(), "test_data", "tiffs", "399"))
    data_type, target, temp_dir = setup
    await create_items(source_dir, data_type, target, temp_dir)
    for collection in collection_store.values():
        await upload_to_local_disk(collection, target)

    assert os.path.isfile(os.path.join(target, "398", "72352.json"))
    assert os.path.isfile(os.path.join(target, "398", "72352.tiff"))
    assert os.path.isfile(os.path.join(target, "398", "collection.json"))

    assert os.path.isfile(os.path.join(target, "399", "72360.json"))
    assert os.path.isfile(os.path.join(target, "399", "72360.tiff"))
    assert os.path.isfile(os.path.join(target, "399", "collection.json"))

    with open(os.path.join(target, "398", "72352.json")) as item_json_file:
        item_metadata = json.load(item_json_file)
    assert item_metadata["properties"]["linz:survey"] == "398"
    assert item_metadata["properties"]["linz:sufi"] == "72352"
    assert item_metadata["id"] == item_metadata["properties"]["linz:sufi"]
    assert (
        item_metadata["assets"]["image"]["file:checksum"]
        == "1220b8f2e22e2d8059ec7c4b327bb695f6a8dc55bdb5f5865b0d2628867f16dca840"
    )
    assert (item_metadata["assets"]["image"]["href"]) == "./398/72352.tiff"
