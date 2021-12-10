Notes for Developers
====================

You can put local schemas here for testing against. See the tests in
topo_processor/metadata/metadata_validators/tests/metadata_validator_stac_local_schema_test.py
For LINZ STAC extensions you will need to alter the stac_extensions stanza, e.g. change

  "definitions": {
    "stac_extensions": {
      "type": "object",
      "required": ["stac_extensions"],
      "properties": {
        "stac_extensions": {
          "type": "array",
          "contains": {
            "const": "https://stac.linz.govt.nz/_STAC_VERSION_/aerial-photo/schema.json"
          }
        }
      }
    },

to reference the local path of the schema:

  "definitions": {
    "stac_extensions": {
      "type": "object",
      "required": ["stac_extensions"],
      "properties": {
        "stac_extensions": {
          "type": "array",
          "contains": {
            "const": "file:///home/your_username/dev/topo-processor/test_data/schemas/aerial-photo-schema.json"
          }
        }
      }
    },
