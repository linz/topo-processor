import re
from typing import Dict


def string_to_number(value):
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


def remove_empty_strings(properties: Dict) -> Dict:
    return {key: value for key, value in properties.items() if value != ""}


def copy_or_original(value):
    """If possible this function returns a boolean,
    if not it returns the original value string.
    """
    clean_value = value.strip().lower()
    if clean_value == "original":
        return True
    if clean_value == "copy":
        return False
    return value


def quarterdate_to_datetime(value):
    """If possible this function converts to RFC3339 datetime format,
    e.g. '2021-01-01T00:00:00.000Z', else returns original value string.
    """
    # Conversion for calendar year quarters to dates
    # Q1 - 2021-01-01T00:00:00.000Z
    # Q2 - 2021-04-01T00:00:00.000Z
    # Q3 - 2021-07-01T00:00:00.000Z
    # Q4 - 2021-10-01T00:00:00.000Z

    quarter_dict_calendar_year = {
        "1": "01",
        "2": "04",
        "3": "07",
        "4": "10",
    }

    re_result = re.search(r"(\d{4})[/][qQ]([1-4])", value)

    # Check the format is what we expect i.e in the form 2020/Q2
    if re_result is not None:

        month = quarter_dict_calendar_year.get(re_result.group(2))
        rfc3339_value = re_result.group(1) + "-" + month + "-01T00:00:00.000Z"
        return rfc3339_value

    return value
