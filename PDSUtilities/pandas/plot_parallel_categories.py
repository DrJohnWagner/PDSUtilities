# Copyright 2022 by Contributors

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from PDSUtilities.plotly import apply_default
from PDSUtilities.plotly import get_font
from PDSUtilities.plotly import ColorblindSafeColormaps

def get_line(df, target, colors):
    line = dict(
        color = colors[0],
        showscale = False,
    )
    if target is not None:
        values = df[target]
        if df[target].dtypes == 'O':
            values = df[target].astype('category').cat.codes
        line['color'] = values
        line['colorscale'] = [
            colors[index % len(colors)] for index in range(len(np.unique(values)))
        ]
    return line

def plot_parallel_categories(df, target = None, columns = None, labels = {},
    width = None, height = None, title = None, colors = 0,
    font = {}, tick_font = {}, label_font = {}, title_font = {}):
    default_font = get_font()
    font = apply_default(default_font, font)
    tick_font = apply_default(font, tick_font)
    label_font = apply_default(font, label_font)
    title_font = apply_default(
        apply_default(font, { 'size': font.get('size', 16) + 4 }),
        title_font
    )
    colors = 0 if colors is None else colors
    if isinstance(colors, int):
        colormaps = ColorblindSafeColormaps()
        colors = colormaps.get_colors(colors)
    #
    if columns is None:
        columns = [column for column in df.columns if df[column].dtypes == 'O']
    if not isinstance(columns, list):
        columns = [column for column in columns]
    if target is not None and target not in columns:
        columns = [target] + columns
    #
    if target is not None:
        if target in columns:
            columns.remove(target)
        columns = [target] + columns
    fig = go.Figure(go.Parcats(
        dimensions = list([
            dict(
                values = df[column],
                label = labels.get(column, column),
                categoryorder = "category ascending",
            ) for column in columns
        ]),
        line = get_line(df, target, colors),
        labelfont = label_font,
        tickfont = tick_font,
    ))
    if title is not None and isinstance(title, str):
        title = { 'text': title, 'x': 0.5, 'xanchor': "center" }
    if title is not None:
        fig.update_layout(title = title, title_font = title_font)
    if width is not None:
        fig.update_layout(width = width)
    if height is not None:
        fig.update_layout(height = height)
    # if template is not None:
    #     fig.update_layout(template = template)
    fig.update_layout(font = font)
    return fig