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
