from datetime import datetime
from typing import Union

import pystac as stac
from linz_logger import get_log

from topo_processor.stac.collection import Collection
from topo_processor.stac.item import Item
from topo_processor.util.time import time_in_ms


async def write_stac_object(custom_stac: Union[Item, Collection], destination: str):
    start_time = time_in_ms()
    if isinstance(custom_stac, Item):
        to_write = stac.Item(
            id=custom_stac.id,
            geometry=None,
            bbox=None,
            datetime=datetime.now(),
            properties=custom_stac.properties,
            stac_extensions=custom_stac.stac_extensions,
        )
        for custom_asset in custom_stac.assets:
            to_write.add_asset(
                key=custom_asset["key"],
                asset=stac.Asset(
                    href=custom_asset["href"], properties=custom_asset["properties"], media_type=custom_asset["media_type"]
                ),
            )

    else:
        to_write = custom_stac.stac_collection

    stac.write_file(obj=to_write, include_self_link=True, dest_href=destination)
    get_log().debug(
        "STAC object written to file",
        duration=time_in_ms() - start_time,
        destination=destination,
    )
