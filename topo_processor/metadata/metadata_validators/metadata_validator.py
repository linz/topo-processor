from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from topo_processor.stac import Item


class MetadataValidator(ABC):

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        pass

    @abstractmethod
    def is_applicable(self, item: Item) -> bool:
        pass

    @abstractmethod
    def validate_metadata(self, item: Item) -> None:
        pass
