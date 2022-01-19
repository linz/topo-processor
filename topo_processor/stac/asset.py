from mimetypes import MimeTypes
from os import path
from typing import TYPE_CHECKING, Any, Dict, Union

import pystac

from topo_processor import stac
from topo_processor.util import Validity, get_file_update_time, multihash_as_hex

from .asset_key import AssetKey

if TYPE_CHECKING:
    from .item import Item


class Asset(Validity):
    source_path: str  # The raw file location on disk
    target: str  # New file name used for uploading
    content_type: str
    needs_upload = bool
    href: str
    properties: Dict[str, str]
    item: "Item"
    key_name: AssetKey

    def __init__(self, source_path: str):
        super().__init__()
        self.source_path = source_path
        self.content_type = None
        self.target = None
        self.needs_upload = True
        self.properties = {}
        self.item = None
        self.key_name = None

    def file_ext(self) -> str:
        return path.splitext(self.target if self.target else self.source_path)[1]

    def get_content_type(self) -> Union[str, None]:
        if self.content_type:
            return self.content_type
        return MimeTypes().guess_type(self.target if self.target else self.source_path)[0]

    def get_checksum(self) -> Any:
        if "file:checksum" not in self.properties:
            self.properties["file:checksum"] = multihash_as_hex(self.source_path)
        return self.properties["file:checksum"]

    def set_output_asset_dates(self, output_path: str) -> None:
        if "created" not in self.properties:
            self.properties["created"] = get_file_update_time(output_path)
            # TODO: process for COG updates not created yet
            self.properties["updated"] = self.properties["created"]
        else:
            self.properties["updated"] = get_file_update_time(output_path)

    def create_stac(self) -> pystac.Asset:
        stac = pystac.Asset(href=self.href, extra_fields=self.properties, media_type=self.get_content_type())
        return stac
