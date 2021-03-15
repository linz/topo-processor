import pystac


class Asset:
    path: str
    key: str
    href: str
    properties = dict
    content_type = pystac.MediaType
    file_ext = str
    upload = bool

    def __init__(self, path, key, properties, content_type, file_ext, upload):
        self.path = path
        self.key = key
        self.href = None
        self.properties = properties
        self.content_type = content_type
        self.file_ext = file_ext
        self.upload = upload

    def create_stac(self) -> pystac.Asset:
        stac = pystac.Asset(href=self.href, properties=self.properties, media_type=self.content_type)
        return stac
