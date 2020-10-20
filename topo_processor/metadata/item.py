from datetime import datetime

import pystac as stac

from .collection import Collection


class Item:

    path: str
    collection: Collection
    stac_item: stac.Item

    def __init__(self, path: str, collection: Collection):
        self.path = path
        self.collection = collection
        self.stac_item = stac.Item(
            stac_extensions=[],
            id="hash",  # TODO
            geometry=None,  # TODO
            bbox=None,  # TODO
            properties={},
            datetime=datetime.now(),
        )
