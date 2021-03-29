import os
from shutil import copyfile

from linz_logger import get_log

from topo_processor.stac import Collection
from topo_processor.util import multihash_as_hex, write_stac_metadata


async def upload_to_local_disk(collection: Collection, target: str):
    if not os.path.isdir(os.path.join(target, collection.title)):
        os.makedirs(os.path.join(target, collection.title))

    stac_collection = collection.create_stac()
    for item in collection.items.values():
        if item.check_validity:
            stac_item = item.create_stac()
            stac_collection.add_item(stac_item)
            for asset in item.assets:
                if asset.needs_upload:
                    asset.properties["file:checksum"] = await multihash_as_hex(asset.path)
                    copyfile(asset.path, os.path.join(target, asset.target))
            await write_stac_metadata(stac_item, os.path.join(target, item.collection.title, f"{item.id}.json"))
        else:
            get_log().warning("Invalid item was not uploaded:", error=item.error_msgs)
        await write_stac_metadata(stac_collection, os.path.join(target, collection.title, "collection.json"))
