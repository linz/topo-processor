from datetime import datetime

import pystac as stac

from .collection import Collection


class Item:

    path: str  # path to data file (input or transformed)
    item_output_path: str  # destination path for stac item json file
    asset_basename: str  # base name of asset (survey/sufi)
    asset_extension: str  # extension of asset (lzw.cog.tiff)
    content_type: str
    collection: Collection
    stac_item: stac.Item

    def __init__(self, path: str, collection: Collection):
        self.path = path
        self.collection = collection
        self.stac_item = stac.Item(
            # add collection back to the constuctor:stac_item after collection.stac_collection is implemented
            id=None,
            geometry=None,
            bbox=None,
            datetime=datetime.now(),
            properties={},
            stac_extensions=[],
        )
