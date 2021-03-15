import pystac


class Asset:
    path: str
    key: str
    href: str
    properties = dict
    content_type = pystac.MediaType
    upload = bool

    def __init__(self, path, key, href, properties, content_type, upload):
        self.path = path
        self.key = key
        self.href = href
        self.properties = properties
        self.content_type = content_type
        self.upload = upload

    def create_stac(self):
        stac = pystac.Asset(href=self.href, properties=self.properties, media_type=self.content_type)
        return stac
