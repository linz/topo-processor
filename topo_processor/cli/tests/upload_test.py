import json
import os
import shutil
import subprocess
from tempfile import mkdtemp

import pytest

import topo_processor.stac as stac


@pytest.fixture(autouse=True)
def setup() -> None:
    """
    This function creates a temporary directory and deletes it after each test.
    See following link for details:
    https://docs.pytest.org/en/stable/fixture.html#yield-fixtures-recommended
    """
    target = mkdtemp()
    yield target
    shutil.rmtree(target)


@pytest.mark.slow
def test_upload_local(setup) -> None: # type: ignore
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
    assert stac.StacExtensions.camera.value in item_metadata["stac_extensions"]
    assert "camera:nominal_focal_length" not in item_metadata["properties"].keys()

    with open(os.path.join(target, "SURVEY_3", "72352.json")) as item_json_file:
        item_metadata = json.load(item_json_file)
    assert item_metadata["properties"]["mission"] == "SURVEY_3"
    assert item_metadata["id"] == "72352"
    assert (
        item_metadata["assets"]["visual"]["file:checksum"]
        == "1220e3e67b095835c5ae8d7b311af25606d3dc0915219f34838e1f0c78b980697ca4"
    )
    assert (item_metadata["assets"]["visual"]["href"]) == "./72352.tiff"
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
    assert stac.StacExtensions.camera.value in item_metadata["stac_extensions"]
