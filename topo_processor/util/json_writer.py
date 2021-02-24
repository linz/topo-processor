from typing import Union

import pystac as stac
from linz_logger import get_log

from topo_processor.stac.collection import Collection
from topo_processor.stac.item import Item
from topo_processor.util.time import time_in_ms


async def write_stac_object(stac_object: Union[Item, Collection], destination: str):
    start_time = time_in_ms()
    if isinstance(stac_object, Item):
        obj = stac_object.stac_item
    else:
        obj = stac_object.stac_collection

    stac.write_file(obj=obj, include_self_link=True, dest_href=destination)
    get_log().debug(
        "STAC object written to file",
        duration=time_in_ms() - start_time,
        destination=destination,
    )
