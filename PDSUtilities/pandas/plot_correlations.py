# Copyright 2022 by Contributors

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PDSUtilities.plotly import apply_default
from PDSUtilities.plotly import get_font
from PDSUtilities.plotly import get_marker
from PDSUtilities.plotly import update_layout
from PDSUtilities.plotly import ColorblindSafeColormaps

def get_labels(labels):
    return { f"F{f}": labels[f] for f in range(len(labels))}

def get_colors(colors, default = 0):
    colors = default if colors is None else colors
    if isinstance(colors, int):
        colors = ColorblindSafeColormaps().get_colors(colors)
    if isinstance(colors, int):
        colors = ColorblindSafeColormaps().get_colors(colors)
    return colors

def get_numrical_columns(columns, target = None):
    if columns is None:
        columns = [column for column in df.columns if df[column].dtypes != 'O']
    if not isinstance(columns, list):
        columns = [column for column in columns]
    if target is not None and target in columns:
        columns.remove(target)
    return columns

def get_correlation_label(correlations, columns, labels, row, col, precision, align = "middle"):
    BR = "<br />"
    col_label = labels.get(columns[col], columns[col])
    row_label = labels.get(columns[row], columns[row])
    cor_label = f"<b>{np.round(correlations.iloc[row, col], precision)}</b>"
    if align == "top":
        return "<span>" + cor_label + BR + col_label + BR + row_label + "</span>"
    if align == "bottom":
        return "<span>" + col_label + BR + row_label + BR + cor_label + "</span>"
    return "<span>" + col_label + BR + cor_label + BR + row_label + "</span>"

def get_mean(values):
    return (0.5*(min(values) + max(values)))

def plot_correlations(df, target = None, columns = None, labels = {},
    width = None, height = None, title = None, precision = 4,
    template = None, colors = 0, marker = {},
    font = {}, tick_font = {}, label_font = {}, title_font = {}):
    #
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
    colors = get_colors(colors)
    columns = get_numrical_columns(columns, target)
    if isinstance(labels, list):
        labels = get_labels(labels)
    rows, cols = len(columns), len(columns)
    correlations = df[columns].corr()
    values = [] if target is None else [value for value in df[target].unique()]
    values = [] if target is None else df[target].unique()
    #
    fig = make_subplots(rows = rows, cols = cols,
        horizontal_spacing = 0.1/cols,
        vertical_spacing = 0.1/rows,
        shared_xaxes = True,
        shared_yaxes = True,
        # print_grid = True,
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
            # Used to center correlation text in
            # the plot as plotly annotations...
            fig.append_trace(
                go.Scatter(
                    x = [get_mean(df[columns[col]])],
                    y = [get_mean(df[columns[row]])],
                    mode = 'markers',
                    marker = get_marker(marker, color = colors[0]),
                    showlegend = False,
                    name = columns[row] + "/" + columns[col],
                    hoverinfo = "skip",
                ),
                col + 1, row + 1
            )
    # Point axes in upper plots to the axes
    # in the corresponding lower plots...
    for row in range(rows):
        for col in range(row):
            # (row, col) corresponds to who we are pointing at...
            x, y = (rows - 1)*cols + col, row*cols
            # So (col, row) is who we are...
            fig.update_xaxes(matches = f"x{x+1}", row = col + 1, col = row + 1)
            fig.update_yaxes(matches = f"y{y+1}", row = col + 1, col = row + 1)
    # Place correlation text centered in
    # the plot as plotly annotations...
    fig.update_layout(annotations = [
        dict(
            x = get_mean(df[columns[col]]),
            y = get_mean(df[columns[row]]),
            xref = "x" + str(col*rows + row + 1),
            yref = "y" + str(col*rows + row + 1),
            text = get_correlation_label(
                correlations, columns, labels, row, col, precision, "middle"
            ),
            showarrow = False,
        ) for row in range(rows) for col in range(row)
    ])
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
    # #
    if target is not None:
        fig.update_layout(legend_itemsizing = 'constant')
        fig.update_layout(legend = dict(
            orientation = 'h', yanchor = 'top', xanchor = 'center', y = 1.07, x = 0.5
        ))
    fig = update_layout(fig, width = width, height = height, title = title, 
        title_font = title_font, font = font, template = template)
    return fig