# Copyright 2022 by Contributors

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_categories_and_counts(df, column, target, value):
    categories = df[column].unique()
    df = df[df[target] == value]
    counts = [df[df[column] == category][column].count() for category in categories]
    return categories, counts

# Plotly is too smart and converts strings to numbers when
# possible but we're smarter: wrap numbers in <span></span>!
def to_string(value):
    if isinstance(value, str):
        return value
    return f"<span>{value}</span>"
    
def get_categories(df, column):
    return [to_string(category) for category in df[column].unique()]

def get_counts(df, column, target = None, value = None):
    categories = df[column].unique()
    if target is not None:
        df = df[df[target] == value]
    counts = [df[df[column] == category][column].count() for category in categories]
    return counts

def get_width(index):
    WIDTHS = [0.0, 0.1, 0.25, 0.35, 0.5, 0.75, 1.0]
    width = WIDTHS[index] if index < len(WIDTHS) else WIDTHS[-1]
    return width

def apply_default(parameter, default):
    if parameter:
        return { **default, **parameter }
    return default

def plot_histograms(df, target, rows = None, cols = None, width = None, height = None,
    title = None, cumulative = None, barmode = "stack", template = None,
    font = {}, title_font = {}, legend_font = {}):
    DEFAULT_FONT = {
        'family': "Verdana, Helvetica, Verdana, Calibri, Garamond, Cambria, Arial",
        'size': 16,
        'color': "#000000"
    }
    font = apply_default(font, DEFAULT_FONT)
    legend_font = apply_default(legend_font, font)
    title_font = apply_default(title_font,
        apply_default({ 'size': font.get('size', 16) + 4 }, font)
    )
    #
    values = [] if target is None else [value for value in df[target].unique()]
    columns = [column for column in df.columns if column != target]
    if target is not None and target in columns:
        columns.remove(target)
    if rows is None and cols is None:
        cols = max(3, min(4, int(np.ceil(np.sqrt(len(columns))))))
        rows = int(np.ceil(len(columns)/cols))
    elif cols is None:
        cols = int(np.ceil(len(columns)/rows))
    elif rows is None:
        rows = int(np.ceil(len(columns)/cols))
    if width is None:
        width = cols*350
    if height is None:
        height = 150 + rows*250
    COLORS = ["#0077BB", "#CC3311", "#33BBEE", "#EE7733", "#009988", "#EE3377", "#BBBBBB"]
    fig = make_subplots(rows = rows, cols = cols,
        horizontal_spacing = 0.06,
        vertical_spacing = 0.12,
        subplot_titles = columns,
    )
    for index, column in enumerate(columns):
        for value in values:
            if df[column].dtypes == np.object or len(df[column].unique()) <= len(COLORS):
                trace = go.Bar(
                    x = get_categories(df, column),
                    y = get_counts(df, column, target, value),
                    marker_color = COLORS[values.index(value) % len(COLORS)],
                    showlegend = index == 0,
                    name = f"{target} = {value}",
                    width = get_width(len(get_categories(df, column))),
                )
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
            else:
                trace = go.Histogram(
                    x = df[df[target] == value][column],
                    marker_color = COLORS[values.index(value) % len(COLORS)],
                    showlegend = index == 0,
                    name = f"{target} = {value}",
                    cumulative_enabled = cumulative,
                )
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
        if target is None:
            if df[column].dtypes == np.object or len(df[column].unique()) <= len(COLORS):
                trace = go.Bar(
                    x = get_categories(df, column),
                    y = get_counts(df, column),
                    marker_color = COLORS[0],
                    showlegend = False,
                    width = get_width(len(get_categories(df, column))),
                )
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
            else:
                trace = go.Histogram(
                    x = df[column],
                    marker_color = COLORS[0],
                    showlegend = False,
                    cumulative_enabled = cumulative,
                )
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
    # barmode = ['stack', 'group', 'overlay', 'relative']
    # barmode = "stack"
    if barmode == "overlay":
        fig.update_traces(opacity=0.75)
    fig.update_annotations(font = font)
    fig.update_traces(marker_line_color = "#000000")
    fig.update_traces(marker_line_width = 0.5)
    if title is not None and isinstance(title, str):
        title = { 'text': title, 'x': 0.5, 'xanchor': "center" }
    if title is not None:
        fig.update_layout(title = title)
    if template is not None:
        fig.update_layout(template = "presentation")
    fig.update_layout(width = width, height = height, barmode = barmode,
        font = font, title_font = title_font, legend_font = legend_font,
        margin = { 't': 160 },
        legend = dict(
            orientation = "h", yanchor = "bottom", y = 1.05, xanchor = "center", x = 0.5
        ),
        # bargap = 0.2, # gap between bars of adjacent location coordinates
        # bargroupgap = 0*0.2, # gap between bars of the same location coordinates
    )
    # This is literally the dumbest thing I've seen in years...
    # This puts space between the ticks and tick labels. SMFH.
    fig.update_yaxes(ticksuffix = " ")
    return fig

fig = plot_histograms(df, target = "HeartDisease", title = "Heart Disease Dataset Histograms", template = "presentation") #, cumulative = True)
fig.show()