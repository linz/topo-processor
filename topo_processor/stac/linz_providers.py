from enum import Enum

import pystac

from .linz_provider import LinzProvider, LinzProviderRole


class LinzProviders(Enum):
    LTTW = LinzProvider(
        name="Toitū Te Whenua LINZ",
        description="The New Zealand Government's lead agency for location and property information, Crown land and managing overseas investment.",
        roles=LinzProviderRole.CUSTODIAN,
        url="https://www.linz.govt.nz/about-linz/what-were-doing/projects/crown-aerial-film-archive-historical-imagery-scanning-project",
    )
    LMPP = LinzProvider(name="Manager Partnership Programmes", roles=LinzProviderRole.MANAGER)
