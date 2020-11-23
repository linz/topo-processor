import os

import pystac as stac
from aiocogeo import COGReader

from topo_processor.metadata.item import Item
from topo_processor.util.tiff import is_tiff
from topo_processor.util.epsg import epsg_code
from .metadata_loader import MetadataLoader


class MetadataLoaderTiff(MetadataLoader):
    name = "loader.imagery.tiff"

    def is_applicable(self, item: Item) -> bool:
        return is_tiff(item.path)

    async def add_metadata(self, item: Item) -> None:
        if "projection" not in item.stac_item.stac_extensions:
            item.stac_item.stac_extensions.append("projection")
        async with COGReader(item.path) as tiff:
            item.stac_item.properties.update({"proj:epsg": epsg_code(tiff.profile["crs"])})
        item.stac_item.add_asset(
            key="image",
            asset=stac.Asset(href=os.path.basename(item.path), properties={}, media_type=stac.MediaType.TIFF),
        )
