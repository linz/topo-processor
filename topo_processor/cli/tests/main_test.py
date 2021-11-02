import json
import os
import shutil
import subprocess
from tempfile import mkdtemp

import pytest

import topo_processor.stac as stac


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


def test_upload_local(setup):
    target = setup
    source = os.path.abspath(os.path.join(os.getcwd(), "test_data", "tiffs"))
    command = os.path.join(os.getcwd(), "upload")
    subprocess.run([command, "-s", source, "-d", "imagery.historic", "-t", target], check=True)

    assert os.path.isfile(os.path.join(target, "SURVEY_3", "72352.json"))
    assert os.path.isfile(os.path.join(target, "SURVEY_3", "72352.tiff"))
    assert os.path.isfile(os.path.join(target, "SURVEY_3", "collection.json"))

    assert os.path.isfile(os.path.join(target, "SURVEY_2", "29659.json"))
    assert os.path.isfile(os.path.join(target, "SURVEY_2", "29659.tif"))
    assert os.path.isfile(os.path.join(target, "SURVEY_2", "collection.json"))

    assert os.path.isfile(os.path.join(target, "SURVEY_1", "72360.json"))
    assert os.path.isfile(os.path.join(target, "SURVEY_1", "72360.tiff"))
    assert os.path.isfile(os.path.join(target, "SURVEY_1", "collection.json"))

    with open(os.path.join(target, "SURVEY_1", "72359.json")) as item_json_file:
        item_metadata = json.load(item_json_file)
    assert item_metadata["properties"]["camera:sequence_number"] == 89555
    assert stac.HistoricalStacExtensions.camera.value in item_metadata["stac_extensions"]
    assert "camera:nominal_focal_length" not in item_metadata["properties"].keys()

    with open(os.path.join(target, "SURVEY_3", "72352.json")) as item_json_file:
        item_metadata = json.load(item_json_file)
    assert item_metadata["properties"]["mission"] == "SURVEY_3"
    assert item_metadata["id"] == "72352"
    assert (
        item_metadata["assets"]["image/tiff; application=geotiff; profile=cloud-optimized"]["file:checksum"]
        == "1220b8f2e22e2d8059ec7c4b327bb695f6a8dc55bdb5f5865b0d2628867f16dca840"
    )
    assert (item_metadata["assets"]["image/tiff; application=geotiff; profile=cloud-optimized"]["href"]) == "./72352.tiff"
    assert len(item_metadata["links"]) == 3
    for link in item_metadata["links"]:
        assert link["rel"] != "self"
        assert link["href"] == "./collection.json"

    with open(os.path.join(target, "SURVEY_3", "collection.json")) as collection_json_file:
        collection_metadata = json.load(collection_json_file)

    assert len(collection_metadata["links"]) == 2
    for link in collection_metadata["links"]:
        assert link["rel"] != "self"
        if link["rel"] == "root":
            assert link["href"] == "./collection.json"
        if link["rel"] == "item":
            assert link["href"] == "./72352.json"

    assert item_metadata["properties"]["camera:sequence_number"] == 89556
    assert item_metadata["properties"]["camera:nominal_focal_length"] == 508
    assert stac.HistoricalStacExtensions.camera.value in item_metadata["stac_extensions"]
