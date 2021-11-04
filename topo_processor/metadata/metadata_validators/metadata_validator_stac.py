from __future__ import annotations

import json
import urllib
from typing import TYPE_CHECKING, Any, Dict

import jsonschema_rs
from linz_logger import get_log
from pystac.errors import STACValidationError

from .metadata_validator import MetadataValidator

if TYPE_CHECKING:
    from topo_processor.stac import Item


class MetadataValidatorStac(MetadataValidator):
    name = "validator.stac"
    validator_cache: Dict[str, Any] = {}

    def get_validator_from_uri(self, schema_uri: str) -> Any:
        if schema_uri not in self.validator_cache:
            response = urllib.request.urlopen(schema_uri)
            schema = response.read()
            self.validator_cache[schema_uri] = jsonschema_rs.JSONSchema.from_str(schema.decode("utf8"))

        validator = self.validator_cache[schema_uri]

        return validator

    def is_applicable(self, item: Item) -> bool:
        return True

    def validate_metadata(self, item: Item) -> None:
        try:
            item.create_stac().validate()

        except STACValidationError as e:
            raise STACValidationError(message=f"Not valid STAC: {e}")

    def validate_metadata_with_report(self, item: Item) -> Dict[str, list[str]]:
        errors_report: Dict[str, list[str]] = {}
        stac_item = item.create_stac().to_dict(include_self_link=False)
        # get `json.dumps` to convert `tuple` into `array` to allow `jsonschema-rs` to validate
        stac_item = json.loads(json.dumps(stac_item))
        schema_uris: list[str] = [item.schema] + stac_item["stac_extensions"]

        get_log().debug(f"{self.name}:validate_metadata_with_report", itemId=stac_item["id"])

        for schema_uri in schema_uris:
            get_log().trace(f"{self.name}:validate_metadata_with_report", schema=schema_uri)
            current_errors = []
            v = self.get_validator_from_uri(schema_uri)

            errors = v.iter_errors(stac_item)

            for error in errors:
                current_errors.append(error.message)
                get_log().warn(f"{self.name}:validate_metadata_with_report", itemId=stac_item["id"], error=error.message)

            if current_errors:
                errors_report[schema_uri] = current_errors

        return errors_report
