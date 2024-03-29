from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, Optional

import rasterio
from linz_logger import get_log
from rasterio.enums import ColorInterp

from topo_processor.file_system.get_fs import get_fs
from topo_processor.stac.stac_extensions import StacExtensions
from topo_processor.util.file_extension import is_tiff

from .metadata_loader import MetadataLoader

if TYPE_CHECKING:
    from topo_processor.stac.asset import Asset


class MetadataLoaderTiff(MetadataLoader):
    name = "metadata.loader.imagery.tiff"

    def is_applicable(self, asset: Optional[Asset] = None) -> bool:
        if asset is None or asset.item is None:
            return False
        return is_tiff(asset.source_path)

    def load_metadata(self, asset: Optional[Asset] = None) -> None:
        if asset:
            fs = get_fs(asset.source_path)
            # FIXME: Should we download the file first as we could need it to do the coggification later?
            # This process takes quiet a long time locally.

            with fs.open(asset.source_path) as f:
                with warnings.catch_warnings(record=True) as w:
                    with rasterio.open(f) as tiff:
                        self.add_epsg(tiff, asset)
                        self.add_bands(tiff, asset)
                for warn in w:
                    get_log().warning(f"Rasterio Warning: {warn.message}", file=asset.source_path, loader=self.name)

    def add_epsg(self, tiff: Any, asset: Asset) -> None:
        if tiff.crs:
            if not tiff.crs.is_epsg_code:
                raise Exception("The code is not a valid EPSG code.")
            crs = tiff.crs.to_epsg()
        else:
            crs = None
        if asset.item:
            asset.item.properties["proj:epsg"] = crs
            asset.item.add_extension(StacExtensions.projection.value)

    def add_bands(self, tiff: Any, asset: Asset) -> None:
        if asset.item:
            asset.item.add_extension(StacExtensions.eo.value)

        if ColorInterp.gray in tiff.colorinterp and len(tiff.colorinterp) == 1:
            asset.properties["eo:bands"] = [{"name": ColorInterp.gray.name, "common_name": "pan"}]
        elif all(band in [ColorInterp.red, ColorInterp.blue, ColorInterp.green] for band in tiff.colorinterp):
            asset.properties["eo:bands"] = [
                {"name": ColorInterp.red.name, "common_name": "red"},
                {"name": ColorInterp.green.name, "common_name": "green"},
                {"name": ColorInterp.blue.name, "common_name": "blue"},
            ]
        elif asset.item:
            asset.item.add_warning(
                msg="Skipped Asset Record",
                cause=self.name,
                e=Exception("stac field 'eo:bands' skipped. Tiff ColorInterp does not match specified values"),
            )
