# Copyright 2022 by Contributors

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
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
            values = LabelEncoder().fit_transform(df[target])
        line['color'] = values
        line['colorscale'] = [
            colors[index] for index in range(len(np.unique(values)))
        ]
    return line

def get_dimension(df, column, labels):
    dimension = dict(
        values = df[column],
        label = labels.get(column, column),
        name = column,
    )
    if df[column].dtypes == 'O':
        le = LabelEncoder()
        dimension['values'] = le.fit_transform(df[column])
        dimension['tickvals'] = np.sort(np.unique(dimension['values']))
        dimension['ticktext'] = le.inverse_transform(dimension['tickvals'])
    elif df[column].dtypes <= np.int64 and len(df[column].unique()) <= 8:
        dimension['tickvals'] = np.sort(df[column].unique())
        dimension['ticktext'] = dimension['tickvals']
    return dimension

def plot_parallel_coordinates(df, target = None, columns = None, labels = {},
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
    #
    colors = 0 if colors is None else colors
    if isinstance(colors, int):
        colormaps = ColorblindSafeColormaps()
        colors = colormaps.get_colors(colors)
    #
    if columns is None:
        columns = [column for column in df.columns if df[column].dtypes != 'O']
    if target is not None and target not in columns:
        columns = [target] + columns
    fig = go.Figure(go.Parcoords(
        dimensions = list([
            get_dimension(df, column, labels)
            for column in columns
        ]),
        line = get_line(df, target, colors),
        labelfont = label_font,
        tickfont = tick_font,
        # This eliminates the range! Set color to background!
        rangefont = { 'size': 1, 'color': "#FFFFFF" }
    ))
    if title is not None and isinstance(title, str):
        title = { 'text': title, 'x': 0.5, 'xanchor': "center" }
    if title is not None:
        fig.update_layout(title = title, title_font = title_font)
    if width is not None:
        fig.update_layout(width = width)
    if height is not None:
        fig.update_layout(height = height)
    fig.update_layout(font = font)
    return fig