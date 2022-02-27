import os

import pystac

from topo_processor.aws.aws_files import build_s3_path, load_file_content, s3_download
from topo_processor.util.configuration import lds_cache_bucket, temp_folder
from topo_processor.util.gzip import decompress_file


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


def get_layer(layer: str) -> str:
    """Download and return local path to the metadata file for the layer"""

    latest_item = get_latest_item(layer)

    exported_asset = latest_item.assets.get("export", None)
    if exported_asset is None:
        raise Exception(f"No exported asset found for lds layer: {layer}")

    asset_path = exported_asset.href.lstrip("./")

    metadata_file_path = f"{temp_folder}/{asset_path}"
    s3_download(build_s3_path(lds_cache_bucket, f"{layer}/{asset_path}"), metadata_file_path)

    if os.path.isfile(metadata_file_path):
        if exported_asset.extra_fields.get("encoding", None) == "gzip":
            decompress_file(metadata_file_path)
        return metadata_file_path
    else:
        raise Exception(f"{metadata_file_path} not found")
