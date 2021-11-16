from enum import Enum


class StacExtensions(str, Enum):
    aerial_photo = "https://stac.linz.govt.nz/v0.0.11/aerial-photo/schema.json"
    camera = "https://stac.linz.govt.nz/v0.0.11/camera/schema.json"
    projection = "https://stac-extensions.github.io/projection/v1.0.0/schema.json"
    file = "https://stac-extensions.github.io/file/v2.0.0/schema.json"
    film = "https://stac.linz.govt.nz/v0.0.11/film/schema.json"
    scanning = "https://stac.linz.govt.nz/v0.0.11/scanning/schema.json"
    eo = "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
    historical_imagery = "https://stac.linz.govt.nz/v0.0.11/historical-imagery/schema.json"
