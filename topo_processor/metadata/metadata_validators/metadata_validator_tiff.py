from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from linz_logger import get_log

from topo_processor.file_system.get_fs import get_fs
from topo_processor.util.file_extension import is_tiff

from .metadata_validator import MetadataValidator

if TYPE_CHECKING:
    from topo_processor.stac.item import Item


class MetadataValidatorTiff(MetadataValidator):
    name = "validator.imagery.tiff"

    def is_applicable(self, item: Item) -> bool:
        for asset in item.assets:
            if is_tiff(asset.source_path):
                return True
        return False

    def validate_metadata(self, item: Item) -> None:

        for asset in item.assets:
            if not is_tiff(asset.source_path):
                continue

            geospatial_type = item.linz_geospatial_type
            eo_bands = asset.properties["eo:bands"]

            with warnings.catch_warnings(record=True) as w:

                # black and white
                if geospatial_type in ["black and white image", "black and white infrared image"]:
                    # check eo:bands matches geospatial_type
                    if len(eo_bands) != 1 or eo_bands[0]["common_name"] != "pan":
                        raise Exception(f"Wrong linz_geospatial_type of '{geospatial_type}' when bands = '{eo_bands}'")
                    else:
                        continue
                # color
                common_names = [common_names["common_name"] for common_names in eo_bands]
                # check linz_geospatial_type matches colorinterp
                if geospatial_type in ["color image", "color infrared image"]:
                    # check eo:bands matches colorinterp
                    if (
                        len(eo_bands) != 3
                        or "red" not in common_names
                        or "green" not in common_names
                        or "blue" not in common_names
                    ):
                        raise Exception(f"Wrong linz_geospatial_type of '{geospatial_type}' when bands = '{eo_bands}'")
                    else:
                        continue
                else:
                    raise Exception(f"Unknown linz_geospatial_type of '{geospatial_type}'")
        for warn in w:
            get_log().warning(f"Warning: {warn.message}", file=asset.source_path, loader=self.name)
