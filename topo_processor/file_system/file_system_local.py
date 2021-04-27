import os
from shutil import copyfile  # not async to be replaced

import pystac

from topo_processor.stac import Asset, Collection, Item
from topo_processor.util import write_stac_metadata

from .file_system import FileSystem


class FileSystemLocal(FileSystem):
    name = "file.system.local"

    async def read(self):
        pass

    async def write(self, collection: Collection, target: str):
        if not os.path.isdir(os.path.join(target, collection.title)):
            os.makedirs(os.path.join(target, collection.title))
        await super().write(collection, target)

    async def write_asset(self, asset: Asset, target: str):
        await asset.get_checksum()
        copyfile(asset.source_path, os.path.join(target, asset.target))

    async def write_item(self, item: Item, target: str):
        stac_item = item.create_stac()
        await write_stac_metadata(stac_item, os.path.join(target, item.collection.title, f"{item.id}.json"))
        return stac_item

    async def write_collection(self, collection: Collection, stac_collection: pystac.collection, target: str):
        await write_stac_metadata(stac_collection, os.path.join(target, collection.title, "collection.json"))

    async def list_(self):
        pass

    async def exists(self):
        pass
