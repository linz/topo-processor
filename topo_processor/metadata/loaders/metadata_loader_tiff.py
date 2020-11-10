import os

import pystac as stac

from topo_processor.metadata.item import Item
from topo_processor.util.tiff import is_tiff
from topo_processor.util.checksum import multihash_as_hex

from .metadata_loader import MetadataLoader


class MetadataLoaderTiff(MetadataLoader):
    name = "loader.imagery.tiff"

    def is_applicable(self, item: Item) -> bool:
        return is_tiff(item.path)

    def add_metadata(self, item: Item) -> None:
        # TODO use GDAL to load metadata from the tiff file if it exists
        item.stac_item.properties["checksum:multihash"] = multihash_as_hex(item.path)
        item.stac_item.add_asset(
            key="image",
            asset=stac.Asset(href=os.path.basename(item.path), properties={}, media_type=stac.MediaType.TIFF),
        )
