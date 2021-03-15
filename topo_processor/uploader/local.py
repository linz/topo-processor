import os
from shutil import copyfile

from topo_processor.stac.collection import Collection
from topo_processor.stac.item import Item
from topo_processor.util import write_stac_metadata


async def upload_to_local_disk(collection: Collection, target: str):
    for item in collection.items:
        await write_stac_metadata(item, f"{target}/{item.metadata_path}")  # for metadata
        await copy_asset(item, target)  # for data
    await write_stac_metadata(collection, f"{target}/{collection.metadata_path}")


async def copy_asset(item: Item, target: str):
    # TODO this is not async
    for asset in item.assets:
        copyfile(asset["path"], os.path.join(target, asset["href"]))
