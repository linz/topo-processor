from __future__ import annotations

from typing import TYPE_CHECKING

import rasterio
from rasterio.enums import ColorInterp

from topo_processor.util import is_tiff

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

    async def validate_metadata(self, item: Item) -> None:
        photo_type = item.properties["linz:photo_type"]
        for asset in item.assets:
            if not is_tiff(asset.source_path):
                continue
            with rasterio.open(asset.source_path) as tiff:
                if ColorInterp.gray in tiff.colorinterp and len(tiff.colorinterp) == 1:
                    if photo_type != "B&W":
                        raise Exception(f"Wrong photo type of {', '.join([color.name for color in tiff.colorinterp])}")
                if all(band in [ColorInterp.red, ColorInterp.blue, ColorInterp.green] for band in tiff.colorinterp):
                    if photo_type != "COLOUR":
                        raise Exception(f"Wrong photo type of {', '.join([color.name for color in tiff.colorinterp])}")
