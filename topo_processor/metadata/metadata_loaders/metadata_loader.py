from abc import ABC, abstractmethod

from topo_processor.stac import Item


class MetadataLoader(ABC):
    @property
    @abstractmethod
    def name(self):
        str

    @abstractmethod
    def is_applicable(self, item: Item) -> bool:
        pass

    @abstractmethod
    async def load_metadata(self, item: Item):
        pass
