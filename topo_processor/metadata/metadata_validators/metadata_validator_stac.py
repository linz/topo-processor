from __future__ import annotations

import warnings
from typing import Any, Dict, Union

import fsspec
import jsonschema_rs
from linz_logger import get_log
from pystac.errors import STACValidationError

from topo_processor.stac.collection import Collection
from topo_processor.stac.item import Item

from .metadata_validator import MetadataValidator


class MetadataValidatorStac(MetadataValidator):
    name = "validator.stac"
    validator_cache: Dict[str, Any] = {}

    def get_validator_from_uri(self, schema_uri: str) -> Any:
        if schema_uri not in self.validator_cache:
            file = fsspec.open(schema_uri, "rt")
            with file as f:
                self.validator_cache[schema_uri] = jsonschema_rs.JSONSchema.from_str(f.read())

        validator = self.validator_cache[schema_uri]

        return validator

    def is_applicable(self, stac_object: Union[Item, Collection]) -> bool:
        return True

    def validate_metadata(self, item: Item) -> None:

        with warnings.catch_warnings(record=True) as w:
            item.create_stac().validate()
            msg = ""
            for warn in w:
                msg = msg + ", " + str(warn.message)

            if msg:
                raise STACValidationError(message=f"Not valid STAC: {msg}")

    def validate_metadata_with_report(self, stac_object: Union[Item, Collection]) -> Dict[str, list[str]]:
        """Validate the STAC object (Item or Collection) against the core json schema and its extensions.
        Return an error report [{schemaURI, [errors]}]
        """
        errors_report: Dict[str, list[str]] = {}
        if isinstance(stac_object, Collection):
            stac_collection = stac_object.create_stac()
            for item in stac_object.items:
                stac_item = stac_object.items[item].create_stac()
                stac_collection.add_item(stac_item)
            stac_object.generate_summaries(stac_collection)
            stac_dict = stac_collection.to_dict(include_self_link=False)
        else:
            stac_dict = stac_object.create_stac().to_dict(include_self_link=False)

        schema_uris: list[str] = [stac_object.schema] + stac_dict["stac_extensions"]

        for schema_uri in schema_uris:
            get_log().trace(f"{self.name}:validate_metadata_with_report", stacId=stac_dict["id"], schema=schema_uri)
            current_errors = []
            v = self.get_validator_from_uri(schema_uri)
            errors = v.iter_errors(stac_dict)

            for error in errors:
                current_errors.append(error.message)
                get_log().warn(f"{self.name}:validate_metadata_with_report", stacId=stac_dict["id"], error=error.message)

            if current_errors:
                errors_report[schema_uri] = current_errors

        return errors_report
