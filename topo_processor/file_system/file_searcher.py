import json
from typing import List

from topo_processor.file_system.manifest import Manifest


def get_file_path_from_survey(survey_id: str, metadata_path: str, manifest_path: str) -> List[str]:
    list_str: List[str] = []
    # load metadata

    # load manifest
    with open(manifest_path) as manifest_json_file:
        manifest_json = json.load(manifest_json_file)
        print(manifest_json["files"])
        manifest = Manifest(**manifest_json)

    for manifest_file in manifest.files:
        list_str.append(manifest_file.path)

    return list_str
