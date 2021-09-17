import json
from urllib.error import HTTPError
from urllib.request import urlopen

from jsonschema import Draft7Validator, validate
from jsonschema.exceptions import ValidationError

from topo_processor.stac import Item

from .metadata_validator import MetadataValidator


class MetadataValidatorStac(MetadataValidator):
    name = "validator.stac"

    def is_applicable(self, item: Item) -> bool:
        return True

    async def validate_metadata(self, item: Item) -> None:
        """
        15/09/2021 - workaround
        when "https://linz.github.io/stac/__STAC_VERSION__/camera/schema.json" works,
        can just use: item.create_stac().validate()
        """
        item_stac = item.create_stac().to_dict()
        for extension in item.stac_extensions:
            try:
                if extension == "https://linz.github.io/stac/__STAC_VERSION__/camera/schema.json":
                    with urlopen("https://raw.githubusercontent.com/linz/stac/master/extensions/camera/schema.json") as f:
                        schema = json.loads(f.read().decode("utf-8"))
                else:
                    with urlopen(extension) as f:
                        schema = json.loads(f.read().decode("utf-8"))
            except HTTPError as e:
                raise Exception("Could not read uri {}".format(extension)) from e

            try:
                validate(item_stac, schema, cls=Draft7Validator)

            except ValidationError as e:
                raise Exception(f"Not valid STAC: {e.message}, {e.schema}, extension: {extension}")
