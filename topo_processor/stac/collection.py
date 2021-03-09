from typing import TYPE_CHECKING, List

import pystac as stac
import ulid

from .data_type import DataType

if TYPE_CHECKING:
    from .item import Item

GLOBAL_PROVIDERS = [
    stac.Provider(name="LINZ", description="Land Information New Zealand", roles=["Host"], url="https://data.linz.govt.nz/")
]


class Collection:
    title: str
    description: str
    license: str
    data_type: DataType
    temp_dir: str
    items: List["Item"]
    providers: List[stac.Provider]
    metadata_file: str
    stac_collection: stac.Collection

    def __init__(self, data_type: DataType, temp_dir: str):
        self.data_type = data_type
        self.temp_dir = temp_dir
        self.items = []
        self.stac_collection = stac.Collection(
            id=ulid.ulid(),
            description=None,
            license=None,
            providers=GLOBAL_PROVIDERS,
            extent=stac.SpatialExtent(bboxes=[0, 0, 0, 0]),
            href=None
        )
        # Required Fields - jeremy's Documentation:
        # - Title
        # - Type
        # - Description
        # - Spatial Coverage/Extent
        # - Metadata Date time
        # - Updated Date time
        # - license
        # - Publisher
        # - creator
        # - licensor
        # - status
        # - Access rights
