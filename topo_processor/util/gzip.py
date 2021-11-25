import gzip
import os

from linz_logger.logger import get_log


def is_gzip_file(file_path: str) -> bool:
    with open(file_path, "rb") as file:
        # gzip magic number == "1f 8b"
        return file.read(2) == b"\x1f\x8b"
        # FIXME: check Header


def decompress_file(file_path: str) -> None:
    input: gzip.GzipFile = None

    try:
        input = gzip.GzipFile(file_path, "rb")
        s = input.read()
    except gzip.BadGzipFile as e:
        get_log().error("File decompression failed", file=file_path, error=e)
        raise e
    finally:
        input.close()

    output = open(file_path, "wb")
    output.write(s)
    output.close()
