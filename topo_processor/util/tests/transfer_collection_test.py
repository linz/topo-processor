import shutil
from datetime import date, datetime
from tempfile import mkdtemp

import dateutil
import pytest

from topo_processor.stac import Asset, Collection, Item
from topo_processor.util.transfer_collection import transfer_collection


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


def test_fail_on_duplicate_assets(setup):
    target = setup
    collection = Collection("fake_title")
    collection.description = "fake_description"
    collection.license = "face_license"
    item = Item("item_id")
    item.datetime = datetime.now()
    collection.add_item(item)
    item.collection = collection

    cog_1 = Asset("./test_data/tiffs/SURVEY_1/CONTROL.tiff")
    cog_1.target = "fake_title/fake_target.tiff"
    item.add_asset(cog_1)

    cog_2 = Asset("test_data/tiffs/SURVEY_1/MULTIPLE_ASSET.tiff")
    cog_2.target = "fake_title/fake_target.tiff"
    item.add_asset(cog_2)

    with pytest.raises(Exception, match=r"./item_id.tiff already exists."):
        transfer_collection(item.collection, target)
