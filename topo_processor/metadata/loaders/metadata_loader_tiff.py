import os

import pystac as stac
from aiocogeo import COGReader

from topo_processor.metadata.item import Item
from topo_processor.util.tiff import is_tiff

from .metadata_loader import MetadataLoader


class MetadataLoaderTiff(MetadataLoader):
    name = "loader.imagery.tiff"

    def is_applicable(self, item: Item) -> bool:
        return is_tiff(item.path)

    async def add_metadata(self, item: Item) -> None:
        async with COGReader(item.path) as tiff:
            item.stac_item.properties.update(tiff.profile)
        item.stac_item.add_asset(
            key="image",
            asset=stac.Asset(href=os.path.basename(item.path), properties={}, media_type=stac.MediaType.TIFF),
        )
