from pyproj import CRS
from pyproj.exceptions import CRSError


def epsg_code(epsg_string: str):
    if epsg_string.lower().startswith("epsg"):
        try:
            return CRS.from_string(epsg_string.lower()).to_epsg()
        except CRSError as e:
            raise Exception(f"{epsg_string} is not a valid EPSG code.") from e
    elif epsg_string.isdigit():
        try:
            return CRS.from_epsg(epsg_string).to_epsg()
        except CRSError as e:
            raise Exception(f"{epsg_string} is not a valid EPSG code.") from e
    else:
        raise Exception(f"{epsg_string} is an invalid format.")

print(epsg_code("epsg:2012"))
