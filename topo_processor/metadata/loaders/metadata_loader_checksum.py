from topo_processor.stac.item import Item
from topo_processor.util.checksum import multihash_as_hex
from topo_processor.util.tiff import is_tiff

from .metadata_loader import MetadataLoader


class MetadataLoaderChecksum(MetadataLoader):
    name = "loader.checksum"

    def is_applicable(self, item: Item) -> bool:
        return is_tiff(item.path)

    async def add_metadata(self, item: Item) -> None:
        if "checksum" not in item.stac_item.stac_extensions:
            item.stac_item.stac_extensions.append("checksum")
        item.stac_item.properties["checksum:multihash"] = await multihash_as_hex(item.path)
