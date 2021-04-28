from abc import ABC, abstractmethod

import pystac
from linz_logger import get_log

from topo_processor.stac import Asset, Collection, Item


class FileSystem(ABC):
    @property
    @abstractmethod
    def name(self):
        str

    @abstractmethod
    async def read(self, directory: str):
        pass

    @abstractmethod
    async def write(self, collection: Collection, target: str):
        stac_collection = collection.create_stac()
        for item in collection.items.values():
            if not item.is_valid:
                get_log().warning("Invalid item was not uploaded:", error=item.error_msgs)
                continue
            for asset in item.assets:
                if not asset.needs_upload:
                    get_log().trace("Asset not uploaded")
                    continue
                await self.write_asset(asset, target)
            stac_collection.add_item(await self.write_item(item, target))
        await self.write_collection(collection, stac_collection, target)

    @abstractmethod
    async def list_(self):
        pass

    @abstractmethod
    async def exists(self):
        pass

    @abstractmethod
    async def write_asset(self, asset: Asset, target: str):
        pass

    @abstractmethod
    async def write_item(self, item: Item, target: str):
        pass

    @abstractmethod
    async def write_collection(self, collection: Collection, stac_collection: pystac.collection, target: str):
        pass
