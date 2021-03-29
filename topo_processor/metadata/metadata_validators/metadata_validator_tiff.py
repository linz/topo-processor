import rasterio
from rasterio.enums import ColorInterp

from topo_processor.stac import Item
from topo_processor.util import is_tiff

from .metadata_validator import MetadataValidator


class MetadataValidatorTiff(MetadataValidator):
    name = "validator.imagery.tiff"

    def is_applicable(self, item: Item) -> bool:
        for asset in item.assets:
            if is_tiff(asset.path):
                return True
        return False

    async def validate_metadata(self, item: Item) -> None:
        photo_type = item.properties["linz:photo_type"]
        for asset in item.assets:
            if not is_tiff(asset.path):
                continue
            with rasterio.open(asset.path) as tiff:
                if ColorInterp.gray in tiff.colorinterp and len(tiff.colorinterp) == 1:
                    if photo_type != "B&W":
                        raise Exception(f"Wrong photo type of {', '.join([color.name for color in tiff.colorinterp])}")
                if all(band in [ColorInterp.red, ColorInterp.blue, ColorInterp.green] for band in tiff.colorinterp):
                    if photo_type != "COLOUR":
                        raise Exception(f"Wrong photo type of {', '.join([color.name for color in tiff.colorinterp])}")
