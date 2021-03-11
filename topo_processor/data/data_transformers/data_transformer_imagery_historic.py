import os

from topo_processor.cog.create_cog import create_cog
from topo_processor.stac import add_asset_image
from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item
from topo_processor.util import is_tiff

from .data_transformer import DataTransformer


class DataTransformerImageryHistoric(DataTransformer):
    name = "compressor.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        if item.collection.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.source_path):
            return False
        return True

    async def transform_data(self, item: Item) -> None:
        if not os.path.isdir(os.path.join(item.collection.temp_dir, item.stac_item.properties["linz:survey"])):
            os.makedirs(os.path.join(item.collection.temp_dir, item.stac_item.properties["linz:survey"]))
        survey_name = os.path.join(item.collection.temp_dir, item.stac_item.properties["linz:survey"])
        compression_method = "lzw"
        item.asset_extension = "lzw.cog.tiff"
        output_path = os.path.join(survey_name, f"{os.path.basename(item.source_path)}.{compression_method}.cog.tiff")
        await create_cog(item.source_path, output_path, compression_method).run()
        item.source_path = output_path  # TODO save this path somewhere else
        await add_asset_image(item)
