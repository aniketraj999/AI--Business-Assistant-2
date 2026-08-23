def normalize_config(config):
    """
    Fill missing values and validate AI response.
    """

    defaults = {
        "chart": "bar",
        "group_by": None,
        "metric": "revenue",
        "aggregation": "sum",
        "top_n": None,
        "sort": "desc",
        "filters": {},
        "analysis": "",
        "recommendation": ""
    }

    if not isinstance(config, dict):
        return defaults

    for key, value in defaults.items():
        config.setdefault(key, value)

    return config
