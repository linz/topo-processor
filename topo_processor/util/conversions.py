import re
import datetime

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

def string_to_boolean(value):
    """If possible this function returns a boolean,
    if not it returns the original value string.
    """
    if value.strip().lower() == "original":
        newvalue = True
        return newvalue
    if value.strip().lower() == "copy":
        newvalue = False
        return newvalue
    return value

def quarterdate_to_datetime(value, datetype):
    """If possible this function converts to RFC3339 datetime format,
    e.g. '2021-01-01T00:00:00.000Z', else returns original value string.
    """
    # Dictionary for quarters to dates
    # Q1 - 2021-01-01T00:00:00.000Z
    # Q2 - 2021-04-01T00:00:00.000Z
    # Q3 - 2021-07-01T00:00:00.000Z
    # Q4 - 2021-10-01T00:00:00.000Z

    quarter_dict = {
        "Q1": "01",
        "Q2": "04",
        "Q3": "07",
        "Q4": "10",
    }

    # Check the format is what we expect i.e in the form 2020/Q2
    if re.match('^[0-9]{4}[/][qQ][1-4]', value):

        date_parts = value.split("/")

        if datetype == "scan":
            try:
                year = int(date_parts[0])
                if year < 2014:
                    return value
            except ValueError:
                return value

        if date_parts[1] in quarter_dict:
            month = quarter_dict.get(date_parts[1])
            rfc3339_value = date_parts[0] + "-" + month + "-01T00:00:00.000Z"
            return rfc3339_value
    else:
        return value
