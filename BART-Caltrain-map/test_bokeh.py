from bokeh.plotting import figure, curdoc
p = figure(); p.line([0,1],[0,1]); curdoc().add_root(p)

