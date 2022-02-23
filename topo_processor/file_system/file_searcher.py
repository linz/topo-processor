from typing import List

from linz_logger import get_log

from topo_processor.file_system.manifest import get_file_path_from_manifest, load_manifest
from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.lds_cache.lds_cache import get_metadata
from topo_processor.util.aws_files import build_s3_path
from topo_processor.util.configuration import historical_imagery_bucket


def get_file_path_from_survey(survey_id: str, manifest_path: str, metadata_path: str = "") -> List[str]:
    list_file_path: List[str] = []
    criteria = {"survey": survey_id}
    metadata = get_metadata(DataType.IMAGERY_HISTORIC, criteria, metadata_path)
    manifest = load_manifest(manifest_path)

    for metadata_row in metadata.values():
        file_name_lower = str(metadata_row["raw_filename"]).lower()
        tmp_list = get_file_path_from_manifest(manifest, ("/" + file_name_lower + ".tif", "/" + file_name_lower + ".tiff"))
        if len(tmp_list) > 1:
            get_log().warn(
                "duplicate_file",
                msg="More than one file found with this name.",
                file_name=file_name_lower,
            )
        elif len(tmp_list) == 1:
            path = build_s3_path(historical_imagery_bucket, tmp_list[0])
            list_file_path.append(path)
        else:
            get_log().warn(
                "file_not_found",
                msg="No file found with this name.",
                file_name=file_name_lower,
            )

    return list_file_path
