import json
import os
import shutil
import subprocess
from tempfile import mkdtemp

import pytest


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
    target = setup
    source = os.path.abspath(os.path.join(os.getcwd(), "test_data", "tiffs", "SURVEY_1"))
    target = setup
    command = os.path.join(os.getcwd(), "upload")
    subprocess.run([command, "-s", source, "-d", "imagery.historic", "-t", target], check=True)

    assert os.path.isfile(os.path.join(target, "SURVEY_3", "72352.json"))
    assert os.path.isfile(os.path.join(target, "SURVEY_3", "72352.tiff"))
    assert os.path.isfile(os.path.join(target, "SURVEY_3", "collection.json"))

    assert os.path.isfile(os.path.join(target, "SURVEY_1", "72360.json"))
    assert os.path.isfile(os.path.join(target, "SURVEY_1", "72360.tiff"))
    assert os.path.isfile(os.path.join(target, "SURVEY_1", "collection.json"))

    with open(os.path.join(target, "SURVEY_3", "72352.json")) as item_json_file:
        item_metadata = json.load(item_json_file)
    assert item_metadata["properties"]["linz:survey"] == "SURVEY_3"
    assert item_metadata["properties"]["linz:sufi"] == "72352"
    assert item_metadata["id"] == item_metadata["properties"]["linz:sufi"]
    assert (
        item_metadata["assets"]["image/tiff; application=geotiff; profile=cloud-optimized"]["file:checksum"]
        == "1220b8f2e22e2d8059ec7c4b327bb695f6a8dc55bdb5f5865b0d2628867f16dca840"
    )
    assert (
        item_metadata["assets"]["image/tiff; application=geotiff; profile=cloud-optimized"]["href"]
    ) == "./SURVEY_3/72352.tiff"
