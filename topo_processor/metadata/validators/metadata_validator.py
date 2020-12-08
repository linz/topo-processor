from abc import ABC, abstractmethod

from topo_processor.metadata.item import Item


class MetadataValidator(ABC):
    @property
    @abstractmethod
    def name(self):
        str

    @abstractmethod
    def is_applicable(self, item: Item) -> bool:
        pass

    @abstractmethod
    async def check_validity(self, item: Item):
        pass
