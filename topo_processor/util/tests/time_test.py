from datetime import datetime
from typing import List

from topo_processor.util.files import get_file_update_time
from topo_processor.util.time import get_min_max_interval


def test_get_min_max_interval():
    dates: List[datetime] = []
    datetime_earliest = datetime.strptime("1918-11-11", "%Y-%m-%d")
    datetime_mid = datetime.strptime("1945-05-08", "%Y-%m-%d")
    datetime_latest = datetime.strptime("1989-11-09", "%Y-%m-%d")
    dates.append(datetime_earliest)
    dates.append(datetime_latest)
    dates.append(datetime_mid)

    assert get_min_max_interval(dates) == [datetime_earliest, datetime_latest]
