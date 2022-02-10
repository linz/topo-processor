from datetime import datetime

import pystac
import pytest
from pystac.collection import Extent, SpatialExtent, TemporalExtent

import topo_processor.stac.lds_cache as lds_cache


def test_get_last_version() -> None:
    extent = Extent(SpatialExtent([0.0]), TemporalExtent([datetime.now(), None]))
    collection: pystac.Collection = pystac.Collection(id="1234", description="fake", extent=extent)
    link_a: pystac.Link = pystac.Link(rel=pystac.RelType.SELF, target="./collection.json")
    link_b: pystac.Link = pystac.Link(rel="layer", target="https://layer/1234")
    link_c: pystac.Link = pystac.Link(rel=pystac.RelType.ITEM, target="./1234_100000.json")
    link_d: pystac.Link = pystac.Link(rel=pystac.RelType.ITEM, target="./1234_100001.json")
    collection.add_links([link_a, link_b, link_c, link_d])

    assert lds_cache.get_latest_item_path(collection).target == "./1234_100001.json"
