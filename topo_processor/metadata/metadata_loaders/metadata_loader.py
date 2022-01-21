from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from topo_processor.stac.asset import Asset


class MetadataLoader(ABC):
    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        pass

    @abstractmethod
    def is_applicable(self, asset: Optional[Asset] = None) -> bool:
        pass

    @abstractmethod
    def load_metadata(self, asset: Optional[Asset] = None) -> None:
        pass
