from linz_logger import get_log

from topo_processor.util.time import time_in_ms

from .get_fs import get_fs


def transfer_file(source_file: str, checksum: str, content_type, target_file: str):
    start_time = time_in_ms()
    with get_fs(source_file).open(source_file, "rb") as f1:
        data = f1.read()
        with get_fs(target_file).open(target_file, "wb", ContentType=content_type, Metadata={"hash": checksum}) as f2:
            f2.write(data)
            get_log().debug(
                "File transferred", source_file=source_file, target_file=target_file, duration=time_in_ms() - start_time
            )
