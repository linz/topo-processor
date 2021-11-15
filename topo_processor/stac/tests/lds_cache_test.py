from typing import Dict

import pystac
import pytest

from topo_processor.stac.lds_cache import LdsCache


def test_get_layer():
    # FIXME: Mock this
    metadata_path: str = ""
    lds_cache: LdsCache = LdsCache("linz-lds-cache", "arn:aws:iam::413910103162:role/internal-user-read")
    metadata_path = lds_cache.get_layer("51002")
    assert metadata_path == "input_data/51002_322142.csv"


def test_get_last_version():
    collection: pystac.Collection = pystac.Collection(id="1234", description="fake", extent=None)
    link_a: pystac.Link = pystac.Link(rel=pystac.RelType.SELF, target="./collection.json")
    link_b: pystac.Link = pystac.Link(rel="layer", target="https://layer/1234")
    link_c: pystac.Link = pystac.Link(rel=pystac.RelType.ITEM, target="./1234_100000.json")
    link_d: pystac.Link = pystac.Link(rel=pystac.RelType.ITEM, target="./1234_100001.json")
    collection.add_links((link_a, link_b, link_c, link_d))

    assert LdsCache.get_last_version(collection) == "100001"


def test_get_collection():
    # FIXME: Mock this
    lds_cache: LdsCache = LdsCache("linz-lds-cache", "arn:aws:iam::413910103162:role/internal-user-read")
    collection: pystac.Collection = lds_cache.get_collection("51002")

    assert collection.id == "sc_01FHPJY0NYZ5T5C6Q5QWK61YB5"


def test_get_metadata_file_path():
    assert LdsCache.get_metadata_file_name("12345", "123456") == "12345_123456.csv"
