import gzip
import os

from linz_logger.logger import get_log


def is_csv(path: str) -> bool:
    return path.endswith(".csv")


def is_gzip_file(file_path: str) -> bool:
    with open(file_path, "rb") as file:
        # gzip magic number == "1f 8b"
        return file.read(2) == b"\x1f\x8b"
        # FIXME: check Header


def empty_dir(dir: str) -> None:
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def decompress_file(file_path: str) -> None:
    input: gzip.GzipFile = None

    try:
        input = gzip.GzipFile(file_path, "rb")
    except gzip.BadGzipFile as e:
        get_log().error(f"An error occurred while trying to decompress {file_path}: {e.strerror}")
        raise e

    s = input.read()
    input.close()

    output = open(file_path, "wb")
    output.write(s)
    output.close()
