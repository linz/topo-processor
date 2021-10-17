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


def string_to_boolean(value, true_values, false_values):
    #     """Find value in lists and return boolean,
    #     else returns the original value string.
    #     """
    clean_value = value.strip().lower()
    if clean_value in true_values:
        return True
    if clean_value in false_values:
        return False
    return value


def quarterdate_to_datetime(value):
    """If possible this function converts quarter e.g. 'Q3' to RFC3339 format,
    e.g. '2021-03-01T00:00:00.000Z', else returns original value string.
    """

    quarter_dict_calendar_year = {
        "1": "01",
        "2": "04",
        "3": "07",
        "4": "10",
    }

    re_result = re.search(r"(\d{4})[/][qQ]([1-4])", value)

    if re_result is not None:

        month = quarter_dict_calendar_year.get(re_result.group(2))
        rfc3339_value = re_result.group(1) + "-" + month + "-01T00:00:00.000Z"
        return rfc3339_value

    return value
