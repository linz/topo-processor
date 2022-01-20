import re
from datetime import datetime
from typing import Any, Dict, List, Union

from dateutil import parser, tz


def string_to_number(value: str) -> Union[float, int, str]:
    """If possible this function returns the int/float of the input value,
    if not it returns the string.
    """
    try:
        int_number = int(value)
        return int_number
    except ValueError:
        try:
            float_number = float(value)
            return float_number
        except ValueError:
            return value


def remove_empty_strings(properties: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in properties.items() if value != ""}


def string_to_boolean(value: str, true_values: List[str], false_values: List[str]) -> Union[bool, str]:
    """Find value in lists and return boolean,
    else returns the original value string.
    """
    clean_value = value.strip().lower()
    if clean_value in true_values:
        return True
    if clean_value in false_values:
        return False
    return value


def nzt_datetime_to_utc_datetime(date: str) -> Union[datetime, Any]:
    utc_tz = tz.gettz("UTC")
    nz_tz = tz.gettz("Pacific/Auckland")

    try:
        nz_time = parser.parse(date).replace(tzinfo=nz_tz)
    except parser.ParserError as err:
        raise Exception(f"Not a valid date: {err}") from err

    utc_time = nz_time.astimezone(utc_tz)

    return utc_time


def quarterdate_to_date_string(value: str) -> str:
    """If possible this function converts quarter e.g. 'Q3' to RFC3339 format,
    e.g. '2021-03-01T00:00:00.000Z', then to UTC, else returns original value string.
    """
    re_result = re.search(r"(\d{4})[/][qQ]([1-4])", value)

    if re_result is not None:

        year = re_result.group(1)
        month = (3 * (int(re_result.group(2)))) - 2

        date_string_nz = f"{year}-{month}-01T00:00:00.000"
        datetime_utc = nzt_datetime_to_utc_datetime(date_string_nz)
        date_string_utc = datetime_utc.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        return date_string_utc

    return value


def historical_imagery_photo_type_to_linz_geospatial_type(photo_type: str) -> str:
    """Find value in dict and return linz_geospatial_type,
    else return the original value string.
    """
    geospatial_type_conversion_table = {
        "B&W": "black and white image",
        "B&W IR": "black and white infrared image",
        "COLOUR": "color image",
        "COLOUR IR": "color infrared image",
    }

    lgs_value = geospatial_type_conversion_table.get(photo_type.strip().upper())
    if lgs_value:
        return lgs_value
    else:
        return photo_type
