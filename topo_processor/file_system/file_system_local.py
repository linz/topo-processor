import asyncio
import os
from shutil import copyfile  # not async to be replaced

import pystac
from linz_logger import get_log

from topo_processor.metadata.metadata_loaders import metadata_loader_repo
from topo_processor.stac import Asset, Collection, Item
from topo_processor.stac.store import get_asset
from topo_processor.util import time_in_ms, write_stac_metadata

from .fs import FileSystem


class FileSystemLocal(FileSystem):
    name = "file.system.local"

    async def read(self, directory: str):
        start_time = time_in_ms()
        assets_to_process = []
        for file_ in os.listdir(directory):
            asset = get_asset(os.path.join(directory, file_))
            assets_to_process.append(metadata_loader_repo.load_metadata(asset))
        await asyncio.gather(*assets_to_process)
        get_log().debug("Assets Created", directory=directory, duration=time_in_ms() - start_time)

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

    async def write_collection(self, collection: Collection, stac_collection: pystac.Collection, target: str):
        await write_stac_metadata(stac_collection, os.path.join(target, collection.title, "collection.json"))

    async def list_(self):
        pass

    async def exists(self):
        pass
