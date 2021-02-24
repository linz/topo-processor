from abc import ABC, abstractmethod

from topo_processor.stac.item import Item


class DataTransformer(ABC):
    @property
    @abstractmethod
    def name(self):
        str

    @abstractmethod
    def is_applicable(self, item: Item) -> bool:
        pass

    @abstractmethod
    async def transform_data(self, item: Item):
        pass
