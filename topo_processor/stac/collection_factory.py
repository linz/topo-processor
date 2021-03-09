from linz_logger import get_log

from topo_processor.util.time import time_in_ms

from .collection import Collection
from .data_type import DataType


async def create_collection(data_type: DataType, temp_dir: str) -> Collection:
    start_time = time_in_ms()
    collection = Collection(data_type, temp_dir)
    get_log().debug(
        "Collection Created", id=collection.stac_collection.id, data_type=data_type, duration=time_in_ms() - start_time
    )
    return collection
