from abc import ABC, abstractmethod

from topo_processor.factory.item import Item


class DataCompressor(ABC):
    @property
    @abstractmethod
    def name(self):
        str

    @abstractmethod
    def is_applicable(self, item: Item) -> bool:
        pass

    @abstractmethod
    async def compress_data(self, item: Item):
        pass
