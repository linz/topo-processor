import os
from datetime import datetime


# TODO: there is no concept of updates yet, so created and updated dates will be the same
def file_dates(path: str) -> str:
    cog_created_date = os.path.getctime(path)
    cog_created_string = datetime.utcfromtimestamp(cog_created_date).strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    return cog_created_string
