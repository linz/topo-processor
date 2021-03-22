import os

import pystac
import ulid
from linz_logger import get_log

from topo_processor.cog.create_cog import create_cog
from topo_processor.stac import Asset, DataType, Item
from topo_processor.util import is_tiff, time_in_ms

from .data_transformer import DataTransformer


class DataTransformerImageryHistoric(DataTransformer):
    name = "compressor.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        if item.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.source_path):
            return False
        return True

    async def transform_data(self, item: Item) -> None:
        survey = item.properties["linz:survey"]
        if not os.path.isdir(os.path.join(item.temp_dir, survey)):
            os.makedirs(os.path.join(item.temp_dir, survey))
        output_path = os.path.join(item.temp_dir, f"{ulid.ulid()}.tiff")
        start_time = time_in_ms()
        await create_cog(item.source_path, output_path, compression_method="lzw").run()
        get_log().debug("Created COG", output_path=output_path, duration=time_in_ms() - start_time)

        item.add_asset(
            "cog",
            Asset(
                key="image",
                path=output_path,
                content_type=pystac.MediaType.COG,
                file_ext=".tiff",
                needs_upload=True,
            ),
        )
        item.assets["source"].needs_upload = False
