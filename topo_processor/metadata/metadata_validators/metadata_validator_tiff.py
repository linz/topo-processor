from __future__ import annotations

from typing import TYPE_CHECKING

import rasterio
from rasterio.enums import ColorInterp

from topo_processor.stac.file_extension import is_tiff

from .metadata_validator import MetadataValidator

if TYPE_CHECKING:
    from topo_processor.stac import Item


class MetadataValidatorTiff(MetadataValidator):
    name = "validator.imagery.tiff"

    def is_applicable(self, item: Item) -> bool:
        for asset in item.assets:
            if is_tiff(asset.source_path):
                return True
        return False

    def validate_metadata(self, item: Item) -> None:

        geospatial_type = item.linz_geospatial_type
        for asset in item.assets:
            if not is_tiff(asset.source_path):
                continue
            eo_bands = asset.properties["eo:bands"]
            with rasterio.open(asset.source_path) as tiff:
                # black and white
                if ColorInterp.gray in tiff.colorinterp and len(tiff.colorinterp) == 1:
                    # check linz_geospatial_type matches colorinterp
                    if geospatial_type not in ["black and white image", "black and white infrared image"]:
                        raise Exception(
                            f"Wrong linz_geospatial_type of '{geospatial_type}' when bands = {', '.join([color.name for color in tiff.colorinterp])}"
                        )
                    # check eo:bands matches colorinterp
                    if len(eo_bands) != 1 or eo_bands[0]["common_name"] != "pan":
                        raise Exception(
                            f"Wrong 'eo:bands' with common name: '{geospatial_type}' when bands = {', '.join([color.name for color in tiff.colorinterp])}"
                        )
                # color
                if all(band in [ColorInterp.red, ColorInterp.blue, ColorInterp.green] for band in tiff.colorinterp):
                    common_names = [common_names["common_name"] for common_names in eo_bands]
                    # check linz_geospatial_type matches colorinterp
                    if geospatial_type not in ["color image", "color infrared image"]:
                        raise Exception(
                            f"Wrong linz_geospatial_type of '{geospatial_type}' when bands = {', '.join([color.name for color in tiff.colorinterp])}"
                        )
                    # check eo:bands matches colorinterp
                    if (
                        len(eo_bands) != 3
                        or "red" not in common_names
                        or "green" not in common_names
                        or "blue" not in common_names
                    ):
                        raise Exception(
                            f"Wrong 'eo:bands' with common name: {geospatial_type} when bands = {', '.join([color.name for color in tiff.colorinterp])}"
                        )
