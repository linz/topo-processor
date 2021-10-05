from __future__ import annotations

import os
from typing import TYPE_CHECKING

from linz_logger import get_log

from .metadata_validator import MetadataValidator

if TYPE_CHECKING:
    from topo_processor.stac import Item


class MetadataValidatorImageryHistoric(MetadataValidator):
    name = "validator.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        return True

    def validate_metadata(self, item: Item) -> None:
        for asset in item.assets:
            parent_folder = os.path.basename(os.path.dirname(asset.source_path))
            if not parent_folder == asset.item.collection.title:
                get_log().info(
                    "Metadata survey does not match image parent folder",
                    metadata_survey=asset.item.collection.title,
                    parent_folder=parent_folder,
                    source_path=asset.source_path,
                )
