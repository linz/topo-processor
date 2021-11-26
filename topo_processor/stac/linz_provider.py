from enum import Enum
from typing import Any, Dict, List, Optional


class LinzProviderRole(str, Enum):

    MANAGER = "manager"
    CUSTODIAN = "custodian"


class LinzProvider:
    # Credit to pyStac as this is mostly the same code as the pystac Provider class

    name: str
    description: Optional[str]
    roles: Optional[List[LinzProviderRole]]
    url: Optional[str]

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        roles: Optional[List[LinzProviderRole]] = None,
        url: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.roles = roles
        self.url = url

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, LinzProvider):
            return NotImplemented
        return self.to_dict() == o.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        """Generate a dictionary representing the JSON of this Provider.

        Returns:
            dict: A serialization of the Provider that can be written out as JSON.
        """
        d: Dict[str, Any] = {"name": self.name}
        if self.description is not None:
            d["description"] = self.description
        if self.roles is not None:
            d["roles"] = self.roles
        if self.url is not None:
            d["url"] = self.url

        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LinzProvider":
        """Constructs an Provider from a dict.

        Returns:
            Provider: The Provider deserialized from the JSON dict.
        """
        return LinzProvider(
            name=d["name"],
            description=d.get("description"),
            roles=d.get(
                "roles",
            ),
            url=d.get("url"),
        )
