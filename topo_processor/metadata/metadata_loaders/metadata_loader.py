from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from topo_processor.stac.asset import Asset


class MetadataLoader(ABC):
    @property
    @abstractmethod
    def name(self) -> None:
        str

    @abstractmethod
    def is_applicable(self, asset: Asset) -> bool:
        pass

    @abstractmethod
    def load_metadata(self, asset: Asset = None, metadata_file: str = "", is_load_all: bool = False) -> None:
        pass
