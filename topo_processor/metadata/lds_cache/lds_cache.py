import os
from typing import Any, Dict, Optional

import pystac
from linz_logger import get_log

from topo_processor.metadata.csv_loader.csv_loader import read_csv
from topo_processor.metadata.data_type import DataType, get_layer_id
from topo_processor.util.aws_files import build_s3_path, load_file_content, s3_download
from topo_processor.util.configuration import lds_cache_bucket, temp_folder
from topo_processor.util.gzip import decompress_file

metadata: Dict[str, Dict[str, Any]] = {}
"""Stores the metadata by layer id"""


def get_latest_item_path(collection: pystac.Collection) -> pystac.Link:
    for link in reversed(collection.get_links()):
        if not link.rel == "item":
            continue
        return link

    raise Exception(f"No version found for Collection {collection.title}")


def get_latest_item(layer: str) -> pystac.Item:
    collection = pystac.Collection.from_dict(load_file_content(lds_cache_bucket, layer + "/collection.json"))
    latest_item = get_latest_item_path(collection)
    latest_item_path = f"{layer}/{latest_item.href.lstrip('./')}"

    return pystac.Item.from_dict(load_file_content(lds_cache_bucket, latest_item_path))


def get_metadata(data_type: str, criteria: Optional[Dict[str, str]] = None, metadata_path: str = "") -> Dict[str, Any]:
    """Return a dictionnary containing the metadata"""
    layer_id = get_layer_id(data_type)

    if not metadata_path:
        if not metadata.get(layer_id):
            latest_item = get_latest_item(layer_id)
            exported_asset = latest_item.assets.get("export", None)

            if exported_asset is None:
                raise Exception(f"No exported asset found for lds layer: {layer_id}")

            asset_path = exported_asset.href.lstrip("./")
            metadata_path = f"{temp_folder}/{asset_path}"
            s3_download(build_s3_path(lds_cache_bucket, f"{layer_id}/{asset_path}"), metadata_path)

            if os.path.isfile(metadata_path):
                if exported_asset.extra_fields.get("encoding", None) == "gzip":
                    decompress_file(metadata_path)
            else:
                raise Exception(f"{metadata_path} not found")

    if os.path.isfile(metadata_path):
        if data_type == DataType.IMAGERY_HISTORIC:
            metadata[layer_id] = read_csv(metadata_path)

    if criteria:
        return filter_metadata(metadata[layer_id], criteria)

    return metadata[layer_id]


def filter_metadata(metadata_to_filter: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
    filtered_dict: Dict[str, Any] = {}
    is_found = False

    for metadata_key, metadata_value in metadata_to_filter.items():
        # TODO Remove this print
        print(f"---------> CRITERIA: {criteria}")
        for criteria_key, criteria_value in criteria.items():
            if metadata_value[criteria_key]:
                if metadata_value[criteria_key] == criteria_value:
                    is_found = True
                else:
                    is_found = False
                    break
            else:
                get_log().warning("filter_metadata", key=criteria_key, msg="Key not found.")
        if is_found:
            filtered_dict[metadata_key] = metadata_value

    return filtered_dict
