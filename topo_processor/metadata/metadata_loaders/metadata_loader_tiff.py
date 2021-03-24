import rasterio

from topo_processor.stac import Item
from topo_processor.util import is_tiff

from .metadata_loader import MetadataLoader


class MetadataLoaderTiff(MetadataLoader):
    name = "metadata.loader.imagery.tiff"

    def is_applicable(self, item: Item) -> bool:
        return is_tiff(item.source_path)

    async def load_metadata(self, item: Item) -> None:
        if "projection" not in item.stac_extensions:
            item.stac_extensions.append("projection")
        with rasterio.open(item.source_path) as tiff:
            if tiff.crs:
                if not tiff.crs.is_epsg_code:
                    raise Exception("The code is not a valid EPSG code.")
                crs = tiff.crs.to_epsg()
            else:
                crs = None
            item.properties.update({"proj:epsg": crs})
