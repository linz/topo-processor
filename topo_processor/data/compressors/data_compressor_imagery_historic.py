import os

from topo_processor.cog.create_cog import create_cog
from topo_processor.factory.data_type import DataType
from topo_processor.factory.item import Item
from topo_processor.util import is_tiff

from .data_compressor import DataCompressor


class DataCompressorImageryHistoric(DataCompressor):
    name = "compressor.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        if item.collection.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.path):
            return False
        return True

    async def compress_data(self, item: Item) -> None:
        input_file = item.path
        output_dir = os.getcwd()  # TODO tempdir?
        volumes = [os.getcwd()]  # TODO tempdir?
        compression_method = "LZW"
        await create_cog(input_file, output_dir, volumes, compression_method)
