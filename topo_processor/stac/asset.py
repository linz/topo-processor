from mimetypes import MimeTypes
from os import path
from typing import TYPE_CHECKING

import pystac

from topo_processor.util import Validity, multihash_as_hex

if TYPE_CHECKING:
    from .item import Item


class Asset(Validity):
    source_path: str  # The raw file location on disk
    target: str  # New file name used for uploading
    content_type: str
    needs_upload = bool
    href: str
    properties = dict
    item: "Item"

    def __init__(self, source_path: str):
        super().__init__()
        self.source_path = source_path
        self.content_type = None
        self.target = None
        self.needs_upload = True
        self.properties = {}
        self.item = None

    def file_ext(self) -> str:
        return path.splitext(self.target if self.target else self.source_path)[1]

    def get_content_type(self) -> str:
        if self.content_type:
            return self.content_type
        return MimeTypes().guess_type(self.target if self.target else self.source_path)[0]

    async def get_checksum(self) -> str:
        if "file:checksum" not in self.properties:
            self.properties["file:checksum"] = await multihash_as_hex(self.source_path)
        return self.properties["file:checksum"]

    def create_stac(self) -> pystac.Asset:
        stac = pystac.Asset(href=self.href, properties=self.properties, media_type=self.get_content_type())
        return stac
