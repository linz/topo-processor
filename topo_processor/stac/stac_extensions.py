from enum import Enum


class StacExtensions(Enum):
    camera = "https://linz.github.io/stac/v0.0.2/camera/schema.json"
    projection = "https://stac-extensions.github.io/projection/v1.0.0/schema.json"
    file = "https://stac-extensions.github.io/file/v2.0.0/schema.json"
    scanning = "https://linz.github.io/stac/v0.0.6/scanning/schema.json"
