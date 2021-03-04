from datetime import datetime

import pystac as stac

from .collection import Collection


class Item:

    path: str
    item_output_path: str
    asset_basename: str
    asset_extension: str
    transformed_asset_extension: str
    content_type: str
    collection: Collection
    stac_item: stac.Item

    def __init__(self, path: str, collection: Collection):
        self.path = path
        self.transformed_data_path = None
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
