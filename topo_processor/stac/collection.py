from typing import TYPE_CHECKING, List

import pystac as stac
import ulid

from .data_type import DataType

GLOBAL_PROVIDERS = [stac.Provider(name="LINZ", description="Land Information New Zealand", roles=["Host"])]
if TYPE_CHECKING:
    from .item import Item


class Collection:
    title: str
    description: str
    license: str
    data_type: DataType
    temp_dir: str
    items: List["Item"]
    providers: List[stac.Provider]
    metadata_path: str

    def __init__(self, data_type: DataType, temp_dir: str):
        self.data_type = data_type
        self.temp_dir = temp_dir
        self.items = []

    def create_stac(self) -> stac.Collection:
        stac_collection = stac.Collection(
            id=ulid.ulid(),
            description=None,
            license=None,
            providers=GLOBAL_PROVIDERS,
            extent=stac.SpatialExtent(bboxes=[0, 0, 0, 0]),
        )
        return stac_collection
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
