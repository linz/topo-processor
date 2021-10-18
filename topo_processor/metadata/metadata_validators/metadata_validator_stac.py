from __future__ import annotations
import json
import urllib
from typing import TYPE_CHECKING, Any, Dict

from pystac.errors import STACValidationError
import fastjsonschema
from linz_logger import get_log

from .metadata_validator import MetadataValidator

if TYPE_CHECKING:
    from topo_processor.stac import Item


class MetadataValidatorStac(MetadataValidator):
    name = "validator.stac"
    validator_cache: Dict[str, Any] = {}

    def get_validator_from_schema_uri(self, schema_uri: str) -> Any:
        if schema_uri not in self.validator_cache:
            response = urllib.request.urlopen(schema_uri)
            s = json.loads(response.read())
            self.validator_cache[schema_uri] = fastjsonschema.compile(s)

        validator = self.validator_cache[schema_uri]

        return validator

    def is_applicable(self, item: Item) -> bool:
        return True

    def validate_metadata(self, item: Item) -> None:
        try:
            item.create_stac().validate()

        except STACValidationError as e:
            raise STACValidationError(message=f"Not valid STAC: {e}")

    def validate_metadata_fast(self, item: Item) -> Dict[str, int]:
        errorsReport: Dict[str, int] = {}
        stac_item = item.create_stac().to_dict(include_self_link=False)

        for schema_uri in stac_item["stac_extensions"]:
            # FIXME: Currently an issue with fastjsonschema lib and this json schema
            if schema_uri != "https://stac-extensions.github.io/file/v2.0.0/schema.json":

                validate = self.get_validator_from_schema_uri(schema_uri=schema_uri)
                try:
                    validate(data=stac_item)
                    get_log().debug(f"{self.name}:validate_metadata_fast", itemId=stac_item["id"])
                except fastjsonschema.JsonSchemaException as err:
                    get_log().warn(f"{self.name}:validate_metadata_fast", itemId=stac_item["id"], error=err)

                    if schema_uri not in errorsReport:
                        errorsReport[schema_uri] = 1
                    else:
                        errorsReport[schema_uri] = errorsReport[schema_uri] + 1

        return errorsReport
