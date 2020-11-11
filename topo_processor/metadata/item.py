import os
from datetime import datetime

import pystac as stac

from .collection import Collection


class Item:

    path: str
    output_filename: str
    collection: Collection
    stac_item: stac.Item

    def __init__(self, path: str, collection: Collection):
        self.path = path
        self.output_filename = os.path.basename(path) + ".json"
        self.collection = collection
        self.stac_item = stac.Item(
            # TODO edit these item fields, add collection back to the constuctor:stac_item after collection.stac_collection is implemented
            id="hash",
            geometry=None,
            bbox=None,
            datetime=datetime.now(),
            properties={},
            stac_extensions=[],
        )
