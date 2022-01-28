from enum import Enum

import pystac


class Providers(Enum):
    TTW = pystac.Provider(
        name="Toitū Te Whenua LINZ",
        description="The New Zealand Government's lead agency for location and property information, Crown land and managing overseas investment.",
        roles=[pystac.ProviderRole.HOST, pystac.ProviderRole.LICENSOR, pystac.ProviderRole.PROCESSOR],
        url="https://www.linz.govt.nz/about-linz/what-were-doing/projects/crown-aerial-film-archive-historical-imagery-scanning-project",
    )
    NZAM = pystac.Provider(
        name="NZ Aerial Mapping",
        description="Aerial survey and geospatial services firm. Went into liquidation in 2014.",
        roles=[pystac.ProviderRole.PRODUCER],
    )
