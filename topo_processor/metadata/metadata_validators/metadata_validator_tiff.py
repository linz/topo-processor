import rasterio
from rasterio.enums import ColorInterp

from topo_processor.stac import Item
from topo_processor.util import is_tiff

from .metadata_validator import MetadataValidator


class MetadataValidatorTiff(MetadataValidator):
    name = "validator.imagery.tiff"

    def is_applicable(self, item: Item) -> bool:
        return is_tiff(item.source_path)

    async def validate_metadata(self, item: Item) -> None:
        photo_type = item.properties["linz:photo_type"]
        with rasterio.open(item.source_path) as tiff:
            if ColorInterp.gray in tiff.colorinterp and len(tiff.colorinterp) == 1:
                if photo_type != "B&W":
                    raise Exception(f"Wrong photo type of {', '.join([color.name for color in tiff.colorinterp])}")
            if all(item in [ColorInterp.red, ColorInterp.blue, ColorInterp.green] for item in tiff.colorinterp):
                if photo_type != "COLOUR":
                    raise Exception(f"Wrong photo type of {', '.join([color.name for color in tiff.colorinterp])}")
