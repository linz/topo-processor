import os

import pystac as stac

from topo_processor.metadata import DataType, create_collection

data_folder = os.path.join(os.getcwd(), "test_data")
collection = create_collection(data_folder, DataType("imagery.historic"))
for item in collection.items:
    stac.write_file(obj=item.stac_item, include_self_link=True, dest_href="build/{}.json".format(item.stac_item.id))
