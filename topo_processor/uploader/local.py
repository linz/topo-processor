import os
from shutil import copyfile

from linz_logger import get_log

from topo_processor.stac.collection import Collection
from topo_processor.util import multihash_as_hex, write_stac_metadata


async def upload_to_local_disk(collection: Collection, target: str):
    if not os.path.isdir(os.path.join(target, collection.title)):
        os.makedirs(os.path.join(target, collection.title))

    for item in collection.items:
        if item.is_valid:
            for asset in item.assets.values():
                if asset.needs_upload:
                    asset.properties["file:checksum"] = await multihash_as_hex(asset.path)
                    copyfile(asset.path, os.path.join(target, item.parent, f"{item.id}{asset.file_ext}"))
            await write_stac_metadata(item, os.path.join(target, item.parent, f"{item.id}{item.file_ext}"))
        else:
            get_log().warning("Invalid item was not uploaded", source_path=item.source_path, error="TODO")  # TODO
    await write_stac_metadata(collection, os.path.join(target, collection.title, f"collection{collection.file_ext}"))
