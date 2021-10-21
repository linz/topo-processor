from __future__ import annotations

import json
import urllib
from typing import TYPE_CHECKING, Any, Dict

from pystac.errors import STACValidationError
from jsonschema import validators, exceptions
from linz_logger import get_log

from .metadata_validator import MetadataValidator

if TYPE_CHECKING:
    from topo_processor.stac import Item


class MetadataValidatorStac(MetadataValidator):
    name = "validator.stac"
    schema_cache: Dict[str, Dict[str, Any]] = {}

    def get_schema_from_uri(self, schema_uri: str) -> Dict[str, Any]:
        if schema_uri not in self.schema_cache:
            response = urllib.request.urlopen(schema_uri)
            s = json.loads(response.read())
            self.schema_cache[schema_uri] = s

        schema = self.schema_cache[schema_uri]

        return schema

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
        get_log().debug(f"{self.name}:validate_metadata_with_report", itemId=stac_item["id"])

        for schema_uri in stac_item["stac_extensions"]:
            current_errors = []
            schema = self.get_schema_from_uri(schema_uri)
            cls = validators.validator_for(schema)

            try:
                cls.check_schema(schema)
            except exceptions.SchemaError as e:
                get_log().error(
                    f"{self.name}:validate_metadata_with_report", itemId=stac_item["id"], schemaURI=schema_uri, error=e
                )

            v = cls(schema)
            errors = sorted(v.iter_errors(stac_item), key=lambda e: e.path)

            for error in errors:
                current_errors.append(error.message)
                get_log().warn(f"{self.name}:validate_metadata_with_report", itemId=stac_item["id"], error=error.message)

            if current_errors:
                errors_report[schema_uri] = current_errors

        return errors_report
