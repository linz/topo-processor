from abc import ABC, abstractmethod

from topo_processor.stac import Collection


class FileSystem(ABC):
    @property
    @abstractmethod
    def name(self):
        str

    @abstractmethod
    async def read(self):
        pass

    @abstractmethod
    async def write(self, collection: Collection, target: str):
        pass

    @abstractmethod
    async def list_(self):
        pass

    @abstractmethod
    async def exists(self):
        pass
