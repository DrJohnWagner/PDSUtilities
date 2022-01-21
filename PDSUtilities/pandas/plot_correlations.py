# Copyright 2022 by Contributors

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PDSUtilities.plotly import apply_default
from PDSUtilities.plotly import get_font
from PDSUtilities.plotly import get_marker
from PDSUtilities.plotly import ColorblindSafeColormaps

# Move this to plotly utilities...
def update_layout(fig, width = None, height = None, title = None, font = {}, template = None):
    if title is not None and isinstance(title, str):
        title = { 'text': title, 'x': 0.5, 'xanchor': "center" }
    if title is not None:
        fig.update_layout(title = title, title_font = title_font)
    if width is not None:
        fig.update_layout(width = width)
    if height is not None:
        fig.update_layout(height = height)
    fig.update_layout(font = font)
    if template is not None:
        fig.update(template = template)
    return fig

def get_labels(labels):
    return { f"F{f}": labels[f] for f in range(len(labels))}

def get_subtitile(correlations, columns, labels, row, col, precision):
    BR = "<br />"
    row_label = "<span>" + labels.get(columns[row], columns[row])
    col_label = labels.get(columns[col], columns[col]) + "</span>"
    correlation = str(np.round(correlations.iloc[row, col], precision))
    return row_label + BR + correlation + BR + col_label

def plot_correlations(df, target = None, columns = None, labels = {},
    width = None, height = None, title = None, precision = 4,
    template = None, colors = 0, marker = {},
    font = {}, tick_font = {}, label_font = {}, title_font = {}):
    default_font = get_font()
    default_marker  = get_marker()
    font = apply_default(default_font, font)
    tick_font = apply_default(font, tick_font)
    label_font = apply_default(font, label_font)
    marker = apply_default(default_marker, marker)
    title_font = apply_default(
        apply_default(font, { 'size': font.get('size', 16) + 4 }),
        title_font
    )
    colors = 0 if colors is None else colors
    if isinstance(colors, int):
        colors = ColorblindSafeColormaps().get_colors(colors)
    if isinstance(colors, int):
        colors = ColorblindSafeColormaps().get_colors(colors)
    if columns is None:
        columns = [column for column in df.columns if df[column].dtypes != 'O']
    if not isinstance(columns, list):
        columns = [column for column in columns]
    if target is not None and target in columns:
        columns.remove(target)
    if isinstance(labels, list):
        labels = get_labels(labels)
    rows, cols = len(columns), len(columns)
    correlations = df[columns].corr()
    values = [] if target is None else [value for value in df[target].unique()]
    subplot_titles = [
        get_subtitile(correlations, columns, labels, row, col, precision) if row < col else ""
        for row in range(len(columns)) for col in range(len(columns))
    ]
    fig = make_subplots(rows = rows, cols = cols,
        horizontal_spacing = 0.1/cols,
        vertical_spacing = 0.1/rows,
        subplot_titles = subplot_titles,
        shared_xaxes = True,
        shared_yaxes = True,
        # print_grid=True,
    )
    for row in range(rows):
        for col in range(row):
            for value in values:
                fig.append_trace(
                    go.Scatter(
                        x = df[df[target] == value][columns[col]],
                        y = df[df[target] == value][columns[row]],
                        mode = 'markers',
                        marker = get_marker(marker, color = colors[value]),
                        name = labels.get(target, target) + " = " + str(value),
                        legendgroup = target + " = " + str(value),
                        showlegend = row == 1 and col == 0,
                    ),
                    row + 1, col + 1
                )
            if target is None:
                fig.append_trace(
                    go.Scatter(
                        x = df[columns[col]],
                        y = df[columns[row]],
                        mode = 'markers',
                        marker = get_marker(marker, color = colors[0]),
                        name = columns[row] + "/" + columns[col],
                        showlegend = False,
                    ),
                    row + 1, col + 1
                )
            fig.append_trace(
                go.Scatter(x = [], y = [],
                    showlegend = False,
                    name = columns[row] + "/" + columns[col],
                ),
                col + 1, row + 1
            )
    # This could be used to change the colour of subplot titles
    # to scale from red to blue indicating correlation...
    # BUT text colormap would need to be different from target colormap
    # to avoid the confusion and chaos...
    # names = {'Plot 1':'2016', 'Plot 2':'2017', 'Plot 3':'2018', 'Plot 4':'2019'}
    # fig.for_each_annotation(lambda a: a.update(text = names[a.text]))
    for row in range(rows):
        fig.update_yaxes(
            title_text = labels.get(columns[row], columns[row]), row = row + 1, col = 1
        )
    for col in range(cols):
        fig.update_xaxes(
            title_text = labels.get(columns[col], columns[col]), row = rows, col = col + 1
        )
    for row in range(rows):
        for col in range(row, cols):
            fig.update_xaxes(showgrid = False, row = row + 1, col = col + 1)
            fig.update_yaxes(showgrid = False, row = row + 1, col = col + 1)
        for col in range(1, cols):
            fig.update_yaxes(ticks = "", row = row + 1, col = col + 1)
    for row in range(rows - 1):
        for col in range(cols):
            fig.update_xaxes(ticks = "", row = row + 1, col = col + 1)
    fig.update_xaxes(
        tickfont = tick_font, title_font = font, linecolor = "black",
        linewidth = 0.5, mirror = True, zeroline = False,
    )
    fig.update_yaxes(
        tickfont = tick_font, title_font = font, linecolor = "black",
        linewidth = 0.5, mirror = True, zeroline = False,
    )
    #
    if target is not None:
        fig.update_layout(legend_itemsizing = 'constant')
        fig.update_layout(legend = dict(
            orientation = 'h', yanchor = 'top', xanchor = 'center', y = 1.07, x = 0.5
        ))
    fig.update_annotations(yshift = -80, font = title_font)
    fig = update_layout(fig, width = width, height = height,
        title = title, font = font, template = template)
    return fig