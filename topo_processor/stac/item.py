from datetime import datetime

import pystac as stac

from .data_type import DataType


class Item:
    source_file: str
    data_type: DataType
    temp_dir = str
    metadata_file: str  # destination path for stac item json file
    asset_basename: str  # base name of asset (survey/sufi)
    asset_extension: str  # extension of asset (lzw.cog.tiff)
    output_dir: str  # directory metadata and data will be stored
    content_type: str
    stac_item: stac.Item
    is_valid: bool

    def __init__(self, source_file: str, data_type: DataType, temp_dir: str):
        self.source_file = source_file
        self.data_type = data_type
        self.temp_dir = temp_dir
        self.stac_item = stac.Item(
            id=None,
            geometry=None,
            bbox=None,
            datetime=datetime.now(),
            properties={},
            stac_extensions=[],
        )
        self.is_valid = False
