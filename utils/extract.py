def get_var(data: dict, var_name: str, default=None):
    """Gets variable value from data dictionary."""
    try:
        for key in str(var_name).split("."):
            try:
                data = data[key]
            except TypeError:
                data = data[int(key)]
        return data
    except (KeyError, TypeError, ValueError):
        return default
