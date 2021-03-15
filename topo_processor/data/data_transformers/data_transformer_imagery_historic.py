import os

import pystac
import ulid

from topo_processor.cog.create_cog import create_cog
from topo_processor.stac.asset import Asset
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
        survey = item.properties["linz:survey"]
        if not os.path.isdir(os.path.join(item.collection.temp_dir, survey)):
            os.makedirs(os.path.join(item.collection.temp_dir, survey))
        output_path = os.path.join(item.collection.temp_dir, f"{ulid.ulid()}.tiff")
        await create_cog(item.source_path, output_path, compression_method="lzw").run()

        item.add_asset(
            Asset(
                key="image",
                path=output_path,
                properties={"file:checksum": None},
                content_type=pystac.MediaType.COG,
                file_ext=".tiff",
                upload=True,
            )
        )
