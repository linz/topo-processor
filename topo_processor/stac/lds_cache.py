import os

import pystac

from topo_processor.util.aws_files import build_s3_path, load_file_content, s3_download
from topo_processor.util.configuration import temp_folder
from topo_processor.util.files import decompress_file, is_gzip_file


class LdsCache:
    bucket: str

    def __init__(self, bucket_name: str):
        self.bucket = bucket_name

    def get_layer(self, layer: str) -> str:
        """Download and return local path to the metadata file for the layer. If no version specified, get the latest version"""

        collection: pystac.Collection = self.get_collection(layer)
        version_number = self.get_last_version(collection)

        metadata_file_name = self.get_metadata_file_name(layer, version_number)
        metadata_file_path = temp_folder + "/" + metadata_file_name
        s3_download(build_s3_path(self.bucket, layer + "/" + metadata_file_name), metadata_file_path)

        if os.path.isfile(metadata_file_path):
            if is_gzip_file(metadata_file_path):
                decompress_file(metadata_file_path)
            return metadata_file_path
        else:
            raise Exception(f"{metadata_file_path} not found")

    def get_collection(self, layer: str) -> pystac.Collection:
        return pystac.Collection.from_dict(load_file_content(self.bucket, layer + "/collection.json"))

    @staticmethod
    def get_last_version(collection: pystac.Collection) -> str:
        # Get the last link item
        href = collection.get_links()[-1].get_href()

        if not href.endswith(".json"):
            raise Exception(f"No version found for Collection {collection.title}")

        item_file_name: str = os.path.basename(href)
        version = item_file_name.replace(".json", "").split("_", 1)[1]

        return version

    @staticmethod
    def get_metadata_file_name(layer: str, version: str) -> str:
        return layer + "_" + version + ".csv"
