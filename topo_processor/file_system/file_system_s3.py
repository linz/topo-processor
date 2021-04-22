from topo_processor.stac import Collection

from .file_system import FileSystem


class FileSystemS3(FileSystem):
    name = "file.system.s3"

    async def read(self):
        pass

    async def write(self, collection: Collection, target: str):
        pass

    async def list_(self):
        pass

    async def exists(self):
        pass
