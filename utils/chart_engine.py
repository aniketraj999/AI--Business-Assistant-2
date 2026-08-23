import plotly.express as px

def build_chart(df, config):

    data = df.copy()

    # Apply filters
    filters = config.get("filters", {})

    for col, value in filters.items():
        if col in data.columns:
            data = data[data[col] == value]

    group = config.get("group_by")
    metric = config.get("metric")
    agg = config.get("aggregation", "sum")

    if group:

        if agg == "sum":
            data = data.groupby(group)[metric].sum().reset_index()

        elif agg == "mean":
            data = data.groupby(group)[metric].mean().reset_index()

        elif agg == "count":
            data = data.groupby(group)[metric].count().reset_index()

        elif agg == "max":
            data = data.groupby(group)[metric].max().reset_index()

        elif agg == "min":
            data = data.groupby(group)[metric].min().reset_index()

    # Sorting
    if metric in data.columns:

        ascending = config.get("sort") != "desc"

        data = data.sort_values(metric, ascending=ascending)

    # Top N
    if config.get("top_n"):

        data = data.head(config["top_n"])

    chart = config["chart"]

    if chart == "bar":
        return px.bar(data, x=group, y=metric)

    elif chart == "line":
        return px.line(data, x=group, y=metric)

    elif chart == "pie":
        return px.pie(data, names=group, values=metric)

    elif chart == "scatter":
        return px.scatter(data, x=group, y=metric)

    elif chart == "histogram":
        return px.histogram(data, x=group)

    return None
