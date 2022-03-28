import json
import warnings
from typing import Any, Dict, Optional, Tuple

import jsonschema
import pystac
from linz_logger import get_log
from pystac import STACObjectType
from pystac.validation.schema_uri_map import DefaultSchemaUriMap, SchemaUriMap
from pystac.validation.stac_validator import STACValidator


class IterErrorsValidator(STACValidator):

    schema_uri_map: SchemaUriMap
    schema_cache: Dict[str, Dict[str, Any]]

    def __init__(self, schema_uri_map: Optional[SchemaUriMap] = None) -> None:

        if schema_uri_map is not None:
            self.schema_uri_map = schema_uri_map
        else:
            self.schema_uri_map = DefaultSchemaUriMap()

        self.schema_cache = {}

    def get_schema_from_uri(self, schema_uri: str) -> Tuple[Dict[str, Any], Any]:
        if schema_uri not in self.schema_cache:
            s = json.loads(pystac.StacIO.default().read_text(schema_uri))
            self.schema_cache[schema_uri] = s

        schema = self.schema_cache[schema_uri]

        resolver = jsonschema.validators.RefResolver(base_uri=schema_uri, referrer=schema, store=self.schema_cache)

        return schema, resolver

    def _validate_from_uri(self, stac_dict: Dict[str, Any], schema_uri: str) -> bool:
        """Return true if there is at least one validation error"""
        is_error = False
        schema, resolver = self.get_schema_from_uri(schema_uri)

        validator = jsonschema.Draft7Validator(schema)
        for error in sorted(validator.evolve(schema=schema).iter_errors(stac_dict), key=str):
            is_error = True
            get_log().error(
                "validation_error",
                err=error.message,
                schemaUri=schema_uri,
            )

        for uri in resolver.store:
            if uri not in self.schema_cache:
                self.schema_cache[uri] = resolver.store[uri]

        return is_error

    def _get_error_message(
        self,
        schema_uri: str,
        stac_object_type: STACObjectType,
        extension_id: Optional[str],
        href: Optional[str],
        stac_id: Optional[str],
    ) -> str:
        s = "Validation failed for {} ".format(stac_object_type)
        if href is not None:
            s += "at {} ".format(href)
        if stac_id is not None:
            s += "with ID {} ".format(stac_id)
        s += "against schema at {}".format(schema_uri)
        if extension_id is not None:
            s += " for STAC extension '{}'".format(extension_id)

        return s

    def validate_core(
        self,
        stac_dict: Dict[str, Any],
        stac_object_type: STACObjectType,
        stac_version: str,
        href: Optional[str] = None,
    ) -> Optional[str]:
        """Validate a core stac object.
        Return value can be None or specific to the implementation.
        Args:
            stac_dict : Dictionary that is the STAC json of the object.
            stac_object_type : The stac object type of the object encoded in
                stac_dict. One of :class:`~pystac.STACObjectType`.
            stac_version : The version of STAC to validate the object against.
            href : Optional HREF of the STAC object being validated.
        Returns:
            str: URI for the JSON schema that was validated against, or None if
                no validation occurred.
        """
        schema_uri = self.schema_uri_map.get_object_schema_uri(stac_object_type, stac_version)

        if schema_uri is None:
            return None
        try:
            is_error = self._validate_from_uri(stac_dict, schema_uri)
            if is_error:
                warnings.warn("StacCoreValidationError")
            return schema_uri
        except Exception as e:
            get_log().error(f"Exception while validating {stac_object_type} href: {href}")
            raise e

    def validate_extension(
        self,
        stac_dict: Dict[str, Any],
        stac_object_type: STACObjectType,
        stac_version: str,
        extension_id: str,
        href: Optional[str] = None,
    ) -> Optional[str]:
        """Validate an extension stac object.
        Return value can be None or specific to the implementation.
        Args:
            stac_dict : Dictionary that is the STAC json of the object.
            stac_object_type : The stac object type of the object encoded in
                stac_dict. One of :class:`~pystac.STACObjectType`.
            stac_version : The version of STAC to validate the object against.
            extension_id : The extension ID to validate against.
            href : Optional HREF of the STAC object being validated.
        Returns:
            str: URI for the JSON schema that was validated against, or None if
                no validation occurred.
        """
        schema_uri = extension_id

        if schema_uri is None:
            return None

        try:
            is_error = self._validate_from_uri(stac_dict, schema_uri)
            if is_error:
                warnings.warn("StacCoreValidationError")
            return schema_uri
        except Exception as e:
            get_log().error(f"Exception while validating {stac_object_type} href: {href}")
            raise e
