from mimetypes import MimeTypes
from os import path
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

import pystac

from topo_processor.util.checksum import multihash_as_hex
from topo_processor.util.configuration import get_version
from topo_processor.util.files import get_file_update_time
from topo_processor.util.valid import Validity

from .asset_key import AssetKey

if TYPE_CHECKING:
    from .item import Item


class Asset(Validity):
    source_path: str  # The raw file location on disk
    target: Optional[str] = None  # New file name used for uploading
    content_type: Optional[str] = None
    needs_upload: bool = True
    href: str
    properties: Dict[str, Any]
    item: Optional["Item"] = None
    key_name: Optional[AssetKey] = None

    def __init__(self, source_path: str):
        super().__init__()
        self.source_path = source_path
        self.properties = {
            "processing:software": {"Topo Processor": get_version()},
        }

    def file_ext(self) -> str:
        return path.splitext(self.target if self.target else self.source_path)[1]

    def get_content_type(self) -> Union[str, None]:
        if self.content_type:
            return self.content_type
        return MimeTypes().guess_type(self.target if self.target else self.source_path)[0]

    def get_checksum(self) -> str:
        if "file:checksum" not in self.properties:
            checksum: str = multihash_as_hex(self.source_path)
            self.properties["file:checksum"] = checksum

        return_value: str = self.properties["file:checksum"]
        return return_value

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
