from PDSUtilities.plotly import ColorblindSafeColormaps

def test_get_count():
    colormaps = ColorblindSafeColormaps()
    assert isinstance(colormaps.get_count(), int)
    assert colormaps.get_count() > 0

def test_get_names():
    colormaps = ColorblindSafeColormaps()
    assert isinstance(colormaps.get_names(), list)
    assert colormaps.get_names() is not None
    assert colormaps.get_names()[-1] == "Grayscale"

def test_get_colors_by_index():
    colormaps = ColorblindSafeColormaps()
    assert isinstance(colormaps.get_colors_by_index(0), list)
    assert isinstance(colormaps.get_colors_by_index(-1), list)
    assert len(colormaps.get_colors_by_index(0)) > 0
    assert len(colormaps.get_colors_by_index(-1)) > 0

def test_get_colors_by_name():
    colormaps = ColorblindSafeColormaps()
    assert isinstance(colormaps.get_colors_by_name("Vibrant"), list)
    assert isinstance(colormaps.get_colors_by_name("Grayscale"), list)
    assert len(colormaps.get_colors_by_name("Vibrant")) > 0
    assert len(colormaps.get_colors_by_name("Grayscale")) > 0

def test_get_colors():
    colormaps = ColorblindSafeColormaps()
    assert isinstance(colormaps.get_colors(0), list)
    assert isinstance(colormaps.get_colors(-1), list)
    assert len(colormaps.get_colors(0)) > 0
    assert len(colormaps.get_colors(-1)) > 0
    assert isinstance(colormaps.get_colors("Vibrant"), list)
    assert isinstance(colormaps.get_colors("Grayscale"), list)
    assert len(colormaps.get_colors("Vibrant")) > 0
    assert len(colormaps.get_colors("Grayscale")) > 0
