import boto3
import json
from typing import Any, Dict, List, Tuple

from topo_processor.util.aws_files import create_s3_manifest, is_s3_path, s3_download
from topo_processor.util.configuration import temp_folder


def load_manifest(manifest_path: str) -> Dict[str, Any]:
    if is_s3_path(manifest_path):
        #if date is older than 3 days create manifest
        create_s3_manifest(manifest_path)
        s3_download(manifest_path, f"{temp_folder}/manifest.json")
        manifest_path = f"{temp_folder}/manifest.json"

    with open(manifest_path) as manifest_json_file:
        manifest: Dict[str, Any] = json.load(manifest_json_file)

    return manifest


def get_file_path_from_manifest(manifest: Dict[str, Any], file_names: Tuple[str, ...]) -> List[str]:
    list_str: List[str] = []

    for manifest_file in manifest["files"]:
        if manifest_file["path"].lower().endswith(file_names):
            list_str.append(manifest_file["path"])

    return list_str


# def create_manifest(manifest_path: str) -> None:

#    manifest = Dict[str, Any]
