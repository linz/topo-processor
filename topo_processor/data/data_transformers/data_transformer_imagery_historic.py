import os

from topo_processor.cog.create_cog import create_cog
from topo_processor.stac import add_asset_image
from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item
from topo_processor.util import is_tiff

from .data_transformer import DataTransformer


class DataTransformerImageryHistoric(DataTransformer):
    name = "data.transformer.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        if item.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.source_file):
            return False
        return True

    async def transform_data(self, item: Item) -> None:
        input_file = os.path.abspath(item.source_file)
        if not os.path.isdir(os.path.join(item.temp_dir, item.stac_item.properties["linz:survey"])):
            os.makedirs(os.path.join(item.temp_dir, item.stac_item.properties["linz:survey"]))
        output_dir = os.path.join(item.temp_dir, item.stac_item.properties["linz:survey"])
        item.asset_extension = "lzw.cog.tiff"
        item.source_file = await create_cog(input_file, output_dir, "lzw")
        await add_asset_image(item)
