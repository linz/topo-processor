from typing import Dict, Tuple

FILE_EXTENSIONS: Dict[str, Tuple[str, ...]] = {"imagery.historic": (".tif", ".tiff")}


def is_extension(file_name: str, extensions: Tuple[str, ...]) -> bool:
    return file_name.lower().endswith(extensions)


def is_csv(path: str) -> bool:
    return is_extension(path, (".csv"))


def is_geopackage(path: str) -> bool:
    return is_extension(path, (".gpkg"))


def is_tiff(path: str) -> bool:
    return is_extension(path, (".tiff", ".tif"))
