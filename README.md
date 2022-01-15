# PDSUtilities
Python Data Science Utilities

## Installation
You can install `PDSUtilities` using `pip`:
```
pip install PDSUtilities
```
or by adding `PDSUtilities` to your `requirements.txt` file.

## Usage
Import the functions you need as follows:
```
from PBSUtilities.xgboost import plot_importance
from PBSUtilities.xgboost import plot_tree
```
See below for sample usage of both of these functions.

## Functions

### Function: plot_importance()
The `plot_importane()` function is a plotly-based replacement
for `xgboost.plot_importance()`. The APIs are similar (though
several parameters have been renamed) but with two key differences.
First, `PDSUtilities.xgboost.plot_importance()` does not rely on `fmap`
to supply feature names, instead exposing a `features` parameter that
that can either be a `list` of feature names or a `dict` that allows mapping of
feature names. And second, `PDSUtilities.xgboost.plot_importance()` does not rely on `matplotlib`
at all, instead using `plotly` for visualisation. This produces
an interactive, publication-quality visualisation that can also
be customised more easily, particularly using `plotly.io` templates.

**The `PDSUtilities.xgboost.plot_importance()` function is a direct
copy/paste/edit modification of `xgboost.plot_importance()` with a few
minor tweaks to the API and relatively light changes to the code. The
xgboost team deserves the vast majority of credit for this code!**
The xgboost license can be found here:
https://github.com/dmlc/xgboost/blob/master/LICENSE

The API is:
```
plot_importance(
	booster, features = {}, width = 0.6, xrange = None, yrange = None,
	title = 'Feature Importance', xlabel = 'F Score', ylabel = 'Features',
	fmap = '', max_features = None, importance_type = 'weight',
	show_grid = True, show_values = True)
```

**Example Usage**
```
import pandas as pd

from xgboost import XGBClassifier
from xgboost import XGBModel
from xgboost import Booster

from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler

from PDSUtilities.xgboost import plot_importance

[...]

df = pd.read_csv("/some/datafile.csv")

xt, xv, yt, yv = train_test_split(
	df.drop("OutputFeature", axis = 1),
	df["OutputFeature"],
)

pipeline = Pipeline(steps = [
    ("transform", ColumnTransformer(
            transformers = [
                ("cat", OrdinalEncoder(), categorical_columns),
                ("num", MinMaxScaler(), numerical_columns)
            ]
        )
    ),
    ("features", SelectKBest()),
    ("classifier", XGBClassifier(
            objective = "binary:logistic",
			eval_metric = "auc",
			use_label_encoder = False
        )
    )
])

parameters = {
    "classifier__colsample_bytree": 0.2,
    "classifier__gamma": 0.4,
    "classifier__learning_rate": 0.1,
    "classifier__max_depth": 4,
    "classifier__n_estimators": 60,
    "features__k": 10,
    "features__score_func": chi2
}
pipeline.set_params(**parameters)
model = pipeline.fit(xt, yt)

[...]

classifier = pipeline["classifier"]
features = [feature for column in xt.columns]

fig = plot_importance(classifier, features = features)
fig.update_layout(template = "presentation", width = 700, height = 600)
fig.show()
```

### Function: plot_tree()
The `plot_tree()` function is a plotly-based replacement for `xgboost.plot_tree()`
that takes visualising booster trees to a whole new visual level. As a result,
the API looks nothing like that of `xgboost.plot_tree()`, though in its
simplest usage, it is almost identical, though again not requiring `fmap`
for adding feature names to the visualisation:
```
from PDSUtilities.xgboost import plot_tree

[...]

booster = pipeline["classifier"].get_booster()

fig = plot_tree(booster, tree = 0, features = features)
fig.show()
```
In this example, `tree` is the tree number and, as with `plot_importance()`,
the `features` parameter can be either a `list` or a `dict`.

Note that the default colours were chosen from a vibrant, colourblind-friendly
palette, but can be completely configured via a number of additional configuration
settings. An additional, handy parameter is `grayscale = True`, which produces
a also colorblind-friendly, grayscale visualisation.

Finally, the `Figure` object returned by `plot_impotance()` can be further customised
via plotly's extensive API.

**Example**
The overall font can be configured by any of the following settings:
```
font = {
	'family': "Garamond, Cambria, Arial, etc",
	'size': 16,
	'color': "#000000"
}
```
These settings can be overridden for nodes, leaves and edges by the
`node_font`, `leaf_font` and `edge_font` settings, respectively. For
example, specifying
```
edge_font = {
	'size': 11,
}
```
would override the `font` setting so that the edge labels would be
11pt Garamond.

Edge colours can be configured via a decision-specific `dict`. For
example, the edge colours corresponding to `grayscale = True`
could be set by:
```
edge_clours = {
	'Yes': "#222222",
	'No': "#777777",
	'Missing': "#AAAAAA",
	'Yes/Missing':  "#222222",
	'No/Missing': "#777777",
}
```
Note that the keys `Yes/Missing` and `No/Missing` correspond to
the case where a branch point has a `Missing` branch that connects
to the same child as `Yes` or `No`, respectively.

Similarly, the edge labels can also be configured via a decision-specific
`dict`. The default is:
```
edge_labels = {
	'Yes': "Yes",
	'No': "No",
	'Missing': "Missing",
	'Yes/Missing': "Yes/Missing",
	'No/Missing': "No/Missing"
}
```
This is handy, for example, when it is known *a priori* that there are
no missing values, in which case setting
```
edge_labels = {
	'Yes/Missing': "Yes/Missing",
	'No/Missing': "No/Missing"
}
```
will lead to a much cleaner looking visualisation.

Node and leaf shapes and lines can also be configured:
```
 node_shape = {
	'type': "rect",
	'fillcolor': "#CBCBCB",
	'opacity': 1.0,
}
node_line = {
	'color': "#666666",
	'width': 1,
	'dash': "solid",
}
leaf_shape = {
	'type': "rounded",
	'fillcolor': "#EDEDED",
	'opacity': 1.0,
}
leaf_line = {
	'color': "#777777",
	'width': 1,
	'dash': "solid",
}
```
Note that `type` can be any of `"rect"`, `"circle"` or
`"rounded"` and that `dash` can be any of `"solid"`, `"dot"`, `"dash"`, `"longdash"`,
`"dashdot"` or `"longdashdot"`.

The edge line, arrow and label properties can also be configured:
```
edge_line = {
	'width': 1.5,
	'dash': "solid",
}
edge_arrow = {
	'arrowhead': 3, # Integer between or equal to 0 and 8
	'arrowsize': 1.5,
}
edge_label = {
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
```
where `dash` is as above and `arrowhead` is an `int` in `range(0, 9)`
that specifies the arrowhead style.

Additionally, `plot_tree()` accepts `width` and `height` parameters
specifying the overall width and height of the visualisation--though the defaults
are reasonably good and tree-size dependent--as well as a `precision` parameter
specifying the number of decimal places displayed when rendering the numbers
in nodes and leaves.

Finally, `plot_tree()` also accepts a `scale` parameter that can be adjusted up or
down if the node and/or leaf labels do not quite fit in their corresponding
shapes. This can occur because `plot_tree()` does not use font metrics for
computing the size of the labels, instead using a reasonable guess. This is
because plotly does not offer this via their API and no python font metric
libraries seemed to offer what was needed. This may be improved in the future
but for now, adjusting `scale` is the preferred method for dealing with this.

As with `plot_impotance()` the returned `Figure` object can be further customised
via plotly's extensive API.

The `plot_tree()` API is:
```
def plot_tree(booster, tree, features = {}, width = None, height = None,
    precision = 4, scale = 0.7, font = None, grayscale = False,
    node_shape = {}, node_line = {}, node_font = {},
    leaf_shape = {}, leaf_line = {}, leaf_font = {},
    edge_labels = {}, edge_colors = {}, edge_arrow = {},
    edge_line = {}, edge_label = {}, edge_font = {}):

```
