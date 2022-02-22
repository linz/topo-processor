import os
from typing import List

from topo_processor.file_system.file_searcher import get_file_path_from_survey
from topo_processor.file_system.get_fs import get_fs
from topo_processor.file_system.get_path_with_protocol import get_path_with_protocol
from topo_processor.metadata.data_type import DataType
from topo_processor.stac.asset import Asset
from topo_processor.stac.file_extension import FILE_EXTENSIONS, is_extension
from topo_processor.stac.store import get_asset
from topo_processor.util.s3 import is_s3_path


def get_assets(source: str, data_type: str, metadata_path: str = "") -> List[Asset]:
    assets_list: List[Asset] = []

    if os.path.isdir(os.path.dirname(source)) or is_s3_path(source):
        fs = get_fs(source)
        for (path, _, files) in fs.walk(source):
            if not files:
                continue
            for file_ in files:
                if not is_extension(file_, FILE_EXTENSIONS[data_type]):
                    continue
                asset_path = get_path_with_protocol(source, fs, path)
                asset = get_asset(f"{asset_path}/{file_}")
                assets_list.append(asset)
    else:
        if data_type == DataType.IMAGERY_HISTORIC:
            # FIXME Where the manifest path should be store in this repository?
            manifest_path = "s3://linz-historical-imagery-staging/manifest.json"
            asset_path_list: List[str] = get_file_path_from_survey(source, manifest_path, metadata_path)
            for path in asset_path_list:
                print(path)

    return assets_list
