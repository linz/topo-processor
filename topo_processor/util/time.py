import time
from datetime import datetime
from typing import List


def time_in_ms() -> float:
    return time.time() * 1000


def get_min_max_interval(times: List[datetime]) -> List[datetime]:
    min_date = None
    max_date = None

    for date in times:
        if not min_date:
            min_date = date
        elif date < min_date:
            min_date = date
        if not max_date:
            max_date = date
        elif date > max_date:
            max_date = date

    return [min_date, max_date]
