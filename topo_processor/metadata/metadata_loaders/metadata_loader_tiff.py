import rasterio

from topo_processor.file_system.get_fs import get_fs
from topo_processor.stac import Asset
from topo_processor.util import is_tiff

from .metadata_loader import MetadataLoader


class MetadataLoaderTiff(MetadataLoader):
    name = "metadata.loader.imagery.tiff"

    def is_applicable(self, asset: Asset) -> bool:
        if asset.item is None:
            return False
        return is_tiff(asset.source_path)

    async def load_metadata(self, asset: Asset) -> None:
        asset.item.add_extension("https://stac-extensions.github.io/projection/v1.0.0/schema.json")
        fs = get_fs(asset.source_path)
        with fs.open(asset.source_path) as f:
            with rasterio.open(f) as tiff:
                if tiff.crs:
                    if not tiff.crs.is_epsg_code:
                        raise Exception("The code is not a valid EPSG code.")
                    crs = tiff.crs.to_epsg()
                else:
                    crs = None
                asset.item.properties.update({"proj:epsg": crs})
