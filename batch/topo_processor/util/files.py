import os
from datetime import datetime


def get_file_update_time(path: str) -> str:
    """Return the time (in ) of the last update of the path metadata
    https://docs.python.org/3.9/library/os.path.html#os.path.getctime
    Here ctime refers to the last metadata change for specified path in UNIX while in Windows, it refers to path creation time."""
    update_ctime = os.path.getctime(path)
    update_time = datetime.utcfromtimestamp(update_ctime).strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    return update_time
