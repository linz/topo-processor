from typing import Dict, Tuple

FILE_EXTENSIONS: Dict[str, Tuple[str, ...]] = {"imagery.historic": (".tif", ".tiff")}


def is_extension(file_name: str, extentions: Tuple[str, ...]) -> bool:
    return file_name.lower().endswith(extentions)


def is_tiff(path: str) -> bool:
    return is_extension(path, (".tiff", ".tif"))
