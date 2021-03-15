import os

import pystac as stac

from topo_processor.cog.create_cog import create_cog
from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item
from topo_processor.util import is_tiff, multihash_as_hex

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

        href = os.path.join(survey, f"{item.id}.lzw.cog.tiff")
        output_path = os.path.join(item.collection.temp_dir, href)
        await create_cog(item.source_path, output_path, compression_method="lzw").run()

        checksum = await multihash_as_hex(output_path)
        asset = {
            "temp_path": output_path,
            "key": "cog",
            "href": href,
            "properties": {"file:checksum": checksum},
            "media_type": stac.MediaType.TIFF,
            "stac_extensions": ["file"],
            "content_type": "image/tiff",
        }
        item.add_asset(asset)
