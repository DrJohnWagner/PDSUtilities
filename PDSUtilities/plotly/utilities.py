DEFAULT_FONT = {
	'family': "Verdana, Helvetica, Verdana, Calibri, Garamond, Cambria, Arial",
	'size': 16,
	'color': "#000000"
}
DEFAULT_SHAPE = {
	'type': "rect",
	'fillcolor': "#FFFFFF",
	'opacity': 1.0,
}
DEFAULT_LINE = {
	'color': "#000000",
	'width': 1,
	# ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
	'dash': "solid",
}
DEFAULT_ARROW = {
    # Integer between or equal to 0 and 8
	'arrowhead': 0,
	# Relative to arrowwidth
	'arrowsize': 1,
	'arrowwidth': 1,
}
DEFAULT_LABEL = {
	'align': "center",
	'bgcolor': "#FFFFFF",
	'bordercolor': "rgba(0,0,0,0)",
	'borderpad': 1,
	'borderwidth': 1,
	'opacity': 1.0,
	'textangle': 0,
	'valign': "middle",
	'visible': True,
}

def apply_default(old_thing, new_thing):
    return { **old_thing, **new_thing } if new_thing is not None else old_thing

def get_font(font = None, family = None, size = None, color = None):
    font = apply_default(DEFAULT_FONT, font)
    font['family'] = family if family is not None else font['family']
    font['size'] = size if size is not None else font['size']
    font['color'] = color if color is not None else font['color']
    return font

def get_shape(shape = None, type = None, fillcolor = None, opacity = None):
    shape = apply_default(DEFAULT_SHAPE, shape)
    shape['type'] = type if type is not None else shape['type']
    shape['fillcolor'] = fillcolor if fillcolor is not None else shape['fillcolor']
    shape['opacity'] = opacity if opacity is not None else shape['opacity']
    return shape

def get_line(line = None, width = None, color = None, dash = None):
    line = apply_default(DEFAULT_LINE, line)
    line['width'] = width if width is not None else line['width']
    line['color'] = color if color is not None else line['color']
    line['dash'] = dash if dash is not None else line['dash']
    return line

def get_arrow(arrow = None, arrowhead = None, arrowsize = None, arrowwidth = None):
    arrow = apply_default(DEFAULT_ARROW, arrow)
    arrow['arrowhead'] = arrowhead if arrowhead is not None else arrow['arrowhead']
    arrow['arrowsize'] = arrowsize if arrowsize is not None else arrow['arrowsize']
    arrow['arrowwidth'] = arrowhead if arrowwidth is not None else arrow['arrowwidth']
    return arrow

# Tweak this API as needed...
def get_label(label = None):
    label = apply_default(DEFAULT_LABEL, label)
    # label['bgcolor'] = bgcolor if bgcolor is not None else label['bgcolor']
    return label