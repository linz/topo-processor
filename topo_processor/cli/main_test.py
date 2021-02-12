import json
import os
import shutil
from tempfile import gettempdir

import pytest

from topo_processor.metadata import DataType, create_collection

from .main import upload_to_local_disk


@pytest.fixture(autouse=True)
def teardown():
    yield
    shutil.rmtree(os.path.join(gettempdir(), "C8054"))


@pytest.mark.asyncio
async def test_local_save_paths():

    source = os.path.join(os.getcwd(), "test_data", "tiffs", "C8054")
    datatype = "imagery.historic"
    target = gettempdir()

    collection = await create_collection(source, DataType(datatype))
    await upload_to_local_disk(collection, target)

    assert os.path.isfile(os.path.join(target, "C8054", "29659.json"))
    assert os.path.isfile(os.path.join(target, "C8054", "29659.tiff"))
    assert os.path.isfile(os.path.join(target, "C8054", "collection.json"))


@pytest.mark.asyncio
async def test_item_contents():

    source = os.path.join(os.getcwd(), "test_data", "tiffs", "C8054")
    datatype = "imagery.historic"
    target = gettempdir()

    collection = await create_collection(source, DataType(datatype))
    await upload_to_local_disk(collection, target)

    with open(os.path.join(target, "C8054", "29659.json")) as item_json_file:
        item_metadata = json.load(item_json_file)

    assert item_metadata["properties"]["linz:survey"] == "C8054"
    assert item_metadata["properties"]["linz:sufi"] == "29659"
    assert item_metadata["id"] == item_metadata["properties"]["linz:sufi"]
    assert (
        item_metadata["properties"]["checksum:multihash"]
        == "1220f7ea9017ef596cc650369493dc3993d9ab5c99055bbc5c7bac9d4e061c5f2f7a"
    )
    assert (item_metadata["assets"]["image"]["href"]) == "C8054/29659.tiff"
