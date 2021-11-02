from enum import Enum


class StacExtensions(Enum):
    aerial_photo = "https://linz.github.io/stac/v0.0.10/aerial-photo/schema.json"
    camera = "https://linz.github.io/stac/v0.0.10/camera/schema.json"
    projection = "https://stac-extensions.github.io/projection/v1.0.0/schema.json"
    file = "https://stac-extensions.github.io/file/v2.0.0/schema.json"
    film = "https://linz.github.io/stac/v0.0.10/film/schema.json"
    scanning = "https://linz.github.io/stac/v0.0.10/scanning/schema.json"
    eo = "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
    historical_imagery = "https://linz.github.io/stac/v0.0.10/historical-imagery/schema.json"
