import os

import pystac

from topo_processor.util.aws_files import build_s3_path, load_file_content, s3_download
from topo_processor.util.configuration import lds_cache_bucket, temp_folder
from topo_processor.util.gzip import decompress_file, is_gzip_file


def get_layer(layer: str) -> str:
    """Download and return local path to the metadata file for the layer. If no version specified, get the latest version"""

    collection: pystac.Collection = get_collection(layer)
    version_number = get_last_version(collection)

    metadata_file_name = get_metadata_file_name(layer, version_number)
    metadata_file_path = temp_folder + "/" + metadata_file_name
    s3_download(build_s3_path(lds_cache_bucket, layer + "/" + metadata_file_name), metadata_file_path)

    if os.path.isfile(metadata_file_path):
        if is_gzip_file(metadata_file_path):
            decompress_file(metadata_file_path)
        return metadata_file_path
    else:
        raise Exception(f"{metadata_file_path} not found")


def get_collection(layer: str) -> pystac.Collection:
    return pystac.Collection.from_dict(load_file_content(lds_cache_bucket, layer + "/collection.json"))


def get_last_version(collection: pystac.Collection) -> str:
    # Get the last link item
    href = collection.get_links()[-1].get_href()

    if not href or not href.endswith(".json"):
        raise Exception(f"No version found for Collection {collection.title}")

    item_file_name: str = os.path.basename(href)
    version = item_file_name.replace(".json", "").split("_", 1)[1]

    return version


def get_metadata_file_name(layer: str, version: str) -> str:
    return layer + "_" + version + ".csv"
