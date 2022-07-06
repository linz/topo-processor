import gzip
from typing import Optional

from linz_logger.logger import get_log


def is_gzip_file(file_path: str) -> bool:
    with open(file_path, "rb") as file:
        # gzip magic number == "1f 8b"
        return file.read(2) == b"\x1f\x8b"


def decompress_file(file_path: str) -> None:
    input: Optional[gzip.GzipFile] = None

    try:
        input = gzip.GzipFile(file_path, "rb")
        s = input.read()
    except gzip.BadGzipFile as e:
        get_log().error("File decompression failed", file=file_path, error=e)
        raise e
    finally:

        if input:
            input.close()

    output = open(file_path, "wb")
    output.write(s)
    output.close()


def decompress_file_gpkg(file_path: str) -> None:
    input: Optional[gzip.GzipFile] = None

    try:
        input = gzip.GzipFile(file_path, "rb")
        print(file_path)
        #s = input.read().decode("utf-8-sig")
        s = input.read().decode()
    except gzip.BadGzipFile as e:
        get_log().error("File decompression failed", file=file_path, error=e)
        raise e
    finally:
        if input:
            input.close()

    output = open(file_path, "w")
    output.write(s)
    output.close()
