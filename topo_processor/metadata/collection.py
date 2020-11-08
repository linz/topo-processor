from typing import TYPE_CHECKING, List

import pystac as stac

from .data_type import DataType

GLOBAL_PROVIDERS = [stac.Provider(name="LINZ", description="Land Information New Zealand", roles=["Host"])]

if TYPE_CHECKING:
    from .item import Item


class Collection:
    """
    A collection of Items
    """

    tilte: str
    description: str
    license: str
    data_type: DataType
    items: List["Item"]
    providers: List[stac.Provider]

    def __init__(self, title: str, description: str, licence: str, data_type: DataType):
        self.title = title
        self.description = description
        self.license = licence
        self.data_type = data_type
        self.items = []
        self.providers = GLOBAL_PROVIDERS

    def stac_collection(self) -> stac.Collection:
        raise Exception("Not Yet Implemented")

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
