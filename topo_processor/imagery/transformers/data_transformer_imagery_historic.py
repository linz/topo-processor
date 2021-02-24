import os

from topo_processor.cog.create_cog import create_cog
from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item
from topo_processor.util import is_tiff

from .data_transformer import DataTransformer


class DataTransformerImageryHistoric(DataTransformer):
    name = "compressor.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        if item.collection.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.path):
            return False
        return True

    async def transform_data(self, item: Item) -> None:
        input_file = os.path.abspath(item.path)
        output_dir = os.getcwd()  # TODO tempdir?
        compression_method = "LZW"
        await create_cog(input_file, output_dir, compression_method)
