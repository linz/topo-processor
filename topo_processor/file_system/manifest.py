from typing import Any, Dict, List

from topo_processor.file_system.manifest_file import ManifestFile


class Manifest(object):
    path: str
    time: int
    size: int
    files: List[ManifestFile] = []

    def __init__(
        self,
        path: str,
        time: int,
        files: List[Dict[str, Any]],
        size: int = 0,
    ) -> None:
        self.path = path
        self.time = time
        self.size = size
        for file in files:
            self.files.append(ManifestFile(**file))
