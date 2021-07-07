import os

from linz_logger import get_log

from topo_processor.file_system.transfer import transfer_file
from topo_processor.file_system.write_json import write_json
from topo_processor.stac import Collection


async def transfer_collection(collection: Collection, target: str):
    stac_collection = collection.create_stac()
    for item in collection.items.values():

        if not item.is_valid():
            get_log().warning("Invalid item was not uploaded:", error=item.log)
            continue

        stac_item = item.create_stac()
        stac_collection.add_item(stac_item)

        for asset in item.assets:
            if asset.needs_upload:
                checksum = await asset.get_checksum()
                transfer_file(asset.source_path, checksum, asset.get_content_type(), os.path.join(target, asset.target))

        # 06/07/2021: Workaround for pystac v1.0.0-beta.2
        json_item = stac_item.to_dict()
        json_item["stac_version"] = "1.0.0"
        write_json(json_item, os.path.join(target, item.collection.title, f"{item.id}.json"))

    # 06/07/2021: Workaround for pystac v1.0.0-beta.2
    json_collection = stac_collection.to_dict()
    json_collection["type"] = "Collection"
    json_collection["stac_version"] = "1.0.0"

    write_json(json_collection, os.path.join(target, collection.title, "collection.json"))
