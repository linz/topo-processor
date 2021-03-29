import rasterio

from topo_processor.stac import Asset
from topo_processor.util import is_tiff

from .metadata_loader import MetadataLoader


class MetadataLoaderTiff(MetadataLoader):
    name = "metadata.loader.imagery.tiff"

    def is_applicable(self, asset: Asset) -> bool:
        if asset.item is None:
            return False
        return is_tiff(asset.path)

    async def load_metadata(self, asset: Asset) -> None:
        asset.item.add_extension("projection")
        with rasterio.open(asset.path) as tiff:
            if tiff.crs:
                if not tiff.crs.is_epsg_code:
                    raise Exception("The code is not a valid EPSG code.")
                crs = tiff.crs.to_epsg()
            else:
                crs = None
            asset.item.properties.update({"proj:epsg": crs})
