import os
from typing import List

from topo_processor.file_system.file_searcher import get_file_path_from_survey
from topo_processor.file_system.get_fs import get_fs
from topo_processor.file_system.get_path_with_protocol import get_path_with_protocol
from topo_processor.metadata.data_type import DataType
from topo_processor.stac.asset import Asset
from topo_processor.stac.file_extension import FILE_EXTENSIONS, is_extension
from topo_processor.stac.store import get_asset
from topo_processor.util.aws_files import build_s3_path
from topo_processor.util.configuration import historical_imagery_bucket
from topo_processor.util.s3 import is_s3_path


def get_assets(source: str, data_type: str, metadata_path: str = "") -> List[Asset]:
    if os.path.isdir(os.path.dirname(source)) or is_s3_path(source):
        return _get_assets_from_directory(source, data_type)
    else:
        if data_type == DataType.IMAGERY_HISTORIC:
            return _get_historical_imagery_assets(source, data_type, metadata_path)
    raise Exception(f"Source is neither Directory or Imagery Historic datatype, source= {source}")

def _get_assets_from_directory(source: str, data_type: str) -> List[Asset]:
    assets_list: List[Asset] = []
    if not is_s3_path(source):
        source = os.path.abspath(source)
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
    return assets_list

def _get_historical_imagery_assets(source: str, data_type: str, metadata_path: str = "") -> List[Asset]:
    assets_list: List[Asset] = []
    manifest_path = build_s3_path(historical_imagery_bucket, "manifest.json")
    asset_path_list: List[str] = get_file_path_from_survey(source, manifest_path, metadata_path)
    for path in asset_path_list:
        if not is_extension(path, FILE_EXTENSIONS[data_type]):
            continue
        asset = get_asset(path)
        assets_list.append(asset)
    return assets_list
