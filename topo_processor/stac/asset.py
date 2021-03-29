from mimetypes import MimeTypes
from os import path
from typing import TYPE_CHECKING

import pystac

from topo_processor.util import Validity

if TYPE_CHECKING:
    from .item import Item


class Asset:
    # The raw file location on disk
    path: str
    # New file name used for uploading
    target: str
    content_type: str

    needs_upload = bool
    href: str
    properties = dict

    item: "Item"

    valid: Validity

    def __init__(self, path: str):
        self.path = path
        self.content_type = None
        self.target = None
        self.needs_upload = True

        self.properties = {}
        self.valid = Validity()

        self.item = None

    def file_ext(self):
        return path.splitext(self.target if self.target else self.path)[1]

    def get_content_type(self):
        if self.content_type:
            return self.content_type
        return MimeTypes().guess_type(self.target if self.target else self.path)[0]

    def create_stac(self) -> pystac.Asset:
        stac = pystac.Asset(href=self.href, properties=self.properties, media_type=self.get_content_type())
        return stac
