from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pystac
import ulid
from linz_logger import get_log

from topo_processor import stac
from topo_processor.cog.create_cog import create_cog
from topo_processor.util import is_tiff, time_in_ms

from .data_transformer import DataTransformer

if TYPE_CHECKING:
    from topo_processor.stac import Item


class DataTransformerImageryHistoric(DataTransformer):
    name = "data.transformer.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        for asset in item.assets:
            if is_tiff(asset.source_path):
                return True
        return False

    def transform_data(self, item: Item) -> None:
        cog_asset_list = []
        for asset in item.assets:
            if not is_tiff(asset.source_path):
                continue
            start_time = time_in_ms()
            output_path = os.path.join(item.collection.get_temp_dir(), f"{ulid.ULID()}.tiff")

            create_cog(asset.source_path, output_path, compression_method="lzw").run()

            get_log().debug("Created COG", output_path=output_path, duration=time_in_ms() - start_time)

            asset.needs_upload = False

            cog_asset = stac.Asset(output_path)
            cog_asset.content_type = pystac.MediaType.COG
            cog_asset.target = asset.target
            cog_asset.properties = asset.properties
            cog_asset_list.append(cog_asset)

        for asset in cog_asset_list:
            item.add_asset(asset)
