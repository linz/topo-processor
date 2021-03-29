import json
import os
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.cli.main import upload_to_local_disk
from topo_processor.stac import collection_store, create_items


@pytest.fixture(autouse=True)
def setup():
    """
    This function creates a temporary directory and deletes it after each test.
    See following link for details:
    https://docs.pytest.org/en/stable/fixture.html#yield-fixtures-recommended
    """
    target = mkdtemp()
    yield target
    shutil.rmtree(target)


@pytest.mark.asyncio
async def test_upload_local(setup):
    source_dir = os.path.abspath(os.path.join(os.getcwd(), "test_data", "tiffs", "399"))
    target = setup
    await create_items(source_dir)
    try:
        for collection in collection_store.values():
            await upload_to_local_disk(collection, target)
    finally:
        for collection in collection_store.values():
            collection.delete_temp_dir()

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
        item_metadata["assets"]["image/tiff; application=geotiff; profile=cloud-optimized"]["file:checksum"]
        == "1220b8f2e22e2d8059ec7c4b327bb695f6a8dc55bdb5f5865b0d2628867f16dca840"
    )
    assert (item_metadata["assets"]["image/tiff; application=geotiff; profile=cloud-optimized"]["href"]) == "./398/72352.tiff"
