from datetime import datetime

import pystac as stac

from .collection import Collection


class Item:

    source_path: str
    metadata_path: str
    asset_basename: str  # base name of asset (survey/sufi)
    asset_extension: str  # extension of asset (lzw.cog.tiff)
    content_type: str
    collection: Collection
    stac_item: stac.Item

    def __init__(self, source_path: str, collection: Collection):
        self.source_path = source_path
        self.collection = collection
        self.stac_item = stac.Item(
            id=None,
            geometry=None,
            bbox=None,
            datetime=datetime.now(),
            properties={},
            stac_extensions=[],
        )
