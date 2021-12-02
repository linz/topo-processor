from enum import Enum


class StacExtensions(str, Enum):
    linz = "https://stac.linz.govt.nz/v0.0.12/linz/schema.json"
    quality = "https://stac.linz.govt.nz/v0.0.12/quality/schema.json"
    historical_imagery = "https://stac.linz.govt.nz/v0.0.12/historical-imagery/schema.json"
    aerial_photo = "https://stac.linz.govt.nz/v0.0.12/aerial-photo/schema.json"
    camera = "https://stac.linz.govt.nz/v0.0.12/camera/schema.json"
    film = "https://stac.linz.govt.nz/v0.0.12/film/schema.json"
    scanning = "https://stac.linz.govt.nz/v0.0.12/scanning/schema.json"
    eo = "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
    file = "https://stac-extensions.github.io/file/v2.0.0/schema.json"
    processing = "https://stac-extensions.github.io/processing/v1.0.0/schema.json"
    projection = "https://stac-extensions.github.io/projection/v1.0.0/schema.json"
    version = "https://stac-extensions.github.io/version/v1.0.0/schema.json"
