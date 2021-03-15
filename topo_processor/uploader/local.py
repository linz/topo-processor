import os
from shutil import copyfile

from topo_processor.stac.collection import Collection
from topo_processor.util import multihash_as_hex, write_stac_metadata


async def upload_to_local_disk(collection: Collection, target: str):
    if not os.path.isdir(os.path.join(target, collection.title)):
        os.mkdir(os.path.join(target, collection.title))

    for item in collection.items:

        for asset in item.assets:
            asset.properties["file:checksum"] = await multihash_as_hex(asset.path)
            copyfile(asset.path, os.path.join(target, asset.href))

        await write_stac_metadata(item, os.path.join(target, item.metadata_path))

    await write_stac_metadata(collection, os.path.join(target, collection.metadata_path))
