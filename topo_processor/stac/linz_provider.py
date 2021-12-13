from enum import Enum
from typing import Any, Dict, List, Optional

from pystac import Provider


class LinzProviderRole(str, Enum):
    """Enumerates the allows values of the LinzProvider "role" field."""

    MANAGER = "manager"
    CUSTODIAN = "custodian"


class LinzProvider(Provider):

    roles: Optional[List[LinzProviderRole]]
    """Optional roles of the provider. Any of manager or custodian.
    LINZ override of pystac.ProviderRole Enum."""

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        roles: Optional[List[LinzProviderRole]] = None,
        url: Optional[str] = None,
        extra_fields: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.description = description
        self.roles = roles
        self.url = url
        self.extra_fields = extra_fields or {}


class LinzProviders(Enum):
    LTTW = LinzProvider(
        name="Toitū Te Whenua LINZ",
        description="The New Zealand Government's lead agency for location and property information, Crown land and managing overseas investment.",
        roles=[LinzProviderRole.CUSTODIAN],
        url="https://www.linz.govt.nz/about-linz/what-were-doing/projects/crown-aerial-film-archive-historical-imagery-scanning-project",
    )
    LMPP = LinzProvider(name="Manager Partnership Programmes", roles=[LinzProviderRole.MANAGER])
