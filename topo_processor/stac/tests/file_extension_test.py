import pytest

from topo_processor.metadata.data_type import DataType
from topo_processor.util.file_extension import FILE_EXTENSIONS, is_extension, is_tiff


def test_is_tiff() -> None:
    file_a = "file.tiff"
    file_b = "file.tif"
    file_c = "file.TIFF"
    file_d = "file.jpg"

    assert is_tiff(file_a) is True
    assert is_tiff(file_b) is True
    assert is_tiff(file_c) is True
    assert is_tiff(file_d) is False


def test_is_extension_imagery_historic() -> None:
    file_a = "file.tiff"
    file_b = "file.tif"
    file_c = "file.TIFF"
    file_d = "file.jpg"

    assert is_extension(file_a, FILE_EXTENSIONS[DataType.IMAGERY_HISTORIC]) is True
    assert is_extension(file_b, FILE_EXTENSIONS[DataType.IMAGERY_HISTORIC]) is True
    assert is_extension(file_c, FILE_EXTENSIONS[DataType.IMAGERY_HISTORIC]) is True
    assert is_extension(file_d, FILE_EXTENSIONS[DataType.IMAGERY_HISTORIC]) is False
