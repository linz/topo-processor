from abc import ABC, abstractmethod

from topo_processor.stac.item import Item


class MetadataValidator(ABC):
    @property
    @abstractmethod
    def name(self):
        str

    @abstractmethod
    def is_applicable(self, item: Item) -> bool:
        pass

    @abstractmethod
    async def validate_metadata(self, item: Item):
        pass
