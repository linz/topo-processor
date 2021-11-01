from __future__ import annotations

from typing import TYPE_CHECKING

import rasterio

from topo_processor import stac
from topo_processor.file_system.get_fs import get_fs
from topo_processor.util import is_tiff

from .metadata_loader import MetadataLoader

if TYPE_CHECKING:
    from topo_processor.stac import Asset


class MetadataLoaderTiff(MetadataLoader):
    name = "metadata.loader.imagery.tiff"

    def is_applicable(self, asset: Asset) -> bool:
        if asset.item is None:
            return False
        return is_tiff(asset.source_path)

    def load_metadata(self, asset: Asset) -> None:
        asset.item.add_extension(stac.StacExtensions.projection.value)

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

    def load_all_metadata(self, metadata_file: str) -> None:
        pass
