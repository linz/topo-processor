from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from topo_processor.stac.asset import Asset


class MetadataLoader(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def is_applicable(self, asset: Union[Asset, None] = None) -> bool:
        pass

    @abstractmethod
    def load_metadata(self, asset: Union[Asset, None] = None) -> None:
        pass
