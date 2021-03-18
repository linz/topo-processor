import pystac


class Asset:
    path: str
    key: str
    content_type = pystac.MediaType
    file_ext = str
    needs_upload = bool
    href: str
    properties = dict

    def __init__(self, path, key, content_type, file_ext, needs_upload):
        self.path = path
        self.key = key
        self.content_type = content_type
        self.file_ext = file_ext
        self.needs_upload = needs_upload

        self.properties = {}

    def create_stac(self) -> pystac.Asset:
        stac = pystac.Asset(href=self.href, properties=self.properties, media_type=self.content_type)
        return stac
