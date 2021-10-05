from pystac.errors import STACValidationError

from topo_processor.stac import Item

from .metadata_validator import MetadataValidator


class MetadataValidatorStac(MetadataValidator):
    name = "validator.stac"

    def is_applicable(self, item: Item) -> bool:
        return True

    def validate_metadata(self, item: Item) -> None:
        try:
            item.create_stac().validate()

        except STACValidationError as e:
            raise STACValidationError(message=f"Not valid STAC: {e}")
