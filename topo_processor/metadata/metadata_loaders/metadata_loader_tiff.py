import rasterio

from topo_processor.stac.item import Item
from topo_processor.util.tiff import is_tiff

from .metadata_loader import MetadataLoader


class MetadataLoaderTiff(MetadataLoader):
    name = "loader.imagery.tiff"

    def is_applicable(self, item: Item) -> bool:
        return is_tiff(item.source_path)

    async def add_metadata(self, item: Item) -> None:
        if "projection" not in item.stac_item.stac_extensions:
            item.stac_item.stac_extensions.append("projection")
        with rasterio.open(item.source_path) as tiff:
            if tiff.crs:
                if not tiff.crs.is_epsg_code:
                    raise Exception("The code is not a valid EPSG code.")
                crs = tiff.crs.to_epsg()
            else:
                crs = None
            item.stac_item.properties.update({"proj:epsg": crs})
            item.asset_extension = "tiff"
            item.content_type = "image/tiff"
