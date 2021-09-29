from __future__ import annotations

from typing import TYPE_CHECKING

from pystac.errors import STACValidationError

from .metadata_validator import MetadataValidator

if TYPE_CHECKING:
    from topo_processor.stac import Item


class MetadataValidatorStac(MetadataValidator):
    name = "validator.stac"

    def is_applicable(self, item: Item) -> bool:
        return True

    async def validate_metadata(self, item: Item) -> None:
        try:
            item.create_stac().validate()

        except STACValidationError as e:
            raise STACValidationError(message=f"Not valid STAC: {e}")
