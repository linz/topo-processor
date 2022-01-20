from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

from linz_logger import get_log

from topo_processor.util.time import time_in_ms

from .metadata_loader import MetadataLoader

if TYPE_CHECKING:
    from topo_processor.stac.asset import Asset


class MetadataLoaderRepository:
    loaders: List[MetadataLoader] = []

    def append(self, loader: MetadataLoader) -> None:
        self.loaders.append(loader)

    def load_metadata(self, asset: Union[Asset, None]) -> None:
        for loader in self.loaders:
            if loader.is_applicable(asset):
                start_time = time_in_ms()
                try:
                    loader.load_metadata(asset)
                    if not asset or not asset.is_valid:
                        break
                except Exception as e:
                    if asset:
                        asset.add_error(str(e), loader.name, e)
                    get_log().warning(f"Metadata Load Failed: {e}", loader=loader.name)
                    return
                get_log().debug(
                    "Metadata Loaded",
                    loader=loader.name,
                    asset=asset.source_path,
                    duration=time_in_ms() - start_time,
                )
