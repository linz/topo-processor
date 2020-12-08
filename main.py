import asyncio
import os

import pystac as stac

from topo_processor.metadata import DataType, create_collection


async def main():
    data_folder = os.path.join(os.getcwd(), "test_data", "tiffs")

    collection = await create_collection(data_folder, DataType("imagery.historic"))

    for item in collection.items:
        stac.write_file(obj=item.stac_item, include_self_link=True, dest_href="build/{}".format(item.output_filename))


asyncio.get_event_loop().run_until_complete(main())
