from typing import Union

import pystac
from linz_logger import get_log

from topo_processor.stac.collection import Collection
from topo_processor.stac.item import Item
from topo_processor.util.time import time_in_ms


async def write_stac_metadata(custom_stac: Union[Item, Collection], destination: str):
    start_time = time_in_ms()
    pystac.write_file(obj=custom_stac.create_stac(), include_self_link=True, dest_href=destination)
    get_log().debug(
        "STAC written to file",
        duration=time_in_ms() - start_time,
        destination=destination,
    )
