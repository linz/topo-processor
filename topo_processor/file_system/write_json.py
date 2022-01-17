import json

import pystac
from linz_logger import get_log

from topo_processor.util import time_in_ms

from .get_fs import get_fs


def write_json(dictionary: str, target_json) -> None:
    start_time = time_in_ms()
    with get_fs(target_json).open(target_json, "w", encoding="utf8", ContentType=pystac.MediaType.JSON) as f1:
        f1.write(json.dumps(dictionary, indent=4, ensure_ascii=False))
        get_log().debug("JSON Written", target_json=target_json, duration=time_in_ms() - start_time)
