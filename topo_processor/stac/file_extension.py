from typing import Dict, List

FILE_EXTENSIONS: Dict[str, List[str]] = {"imagery.historic": [".tif", ".tiff"]}


def is_extension(file_name: str, extentions: List[str]) -> bool:
    return file_name.lower().endswith(extentions)


def is_tiff(path: str) -> bool:
    return is_extension(path, (".tiff", ".tif"))
