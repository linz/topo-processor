from mimetypes import MimeTypes
from typing import TYPE_CHECKING, List

import pystac
import ulid

from .data_type import DataType

GLOBAL_PROVIDERS = [pystac.Provider(name="LINZ", description="Land Information New Zealand", roles=["Host"])]
if TYPE_CHECKING:
    from .item import Item


class Collection:
    title: str
    description: str
    license: str
    data_type: DataType
    temp_dir: str
    items: List["Item"]
    providers: List[pystac.Provider]
    metadata_path: str
    content_type = pystac.MediaType

    def __init__(self, data_type: DataType, temp_dir: str):
        self.data_type = data_type
        self.temp_dir = temp_dir
        self.items = []
        self.content_type = pystac.MediaType.JSON
        self.file_ext = MimeTypes().guess_extension(self.content_type)

    def create_stac(self) -> pystac.Collection:
        stac = pystac.Collection(
            id=ulid.ulid(),
            description=None,
            license=None,
            providers=GLOBAL_PROVIDERS,
            extent=pystac.SpatialExtent(bboxes=[0, 0, 0, 0]),
        )
        return stac
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
