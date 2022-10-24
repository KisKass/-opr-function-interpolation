import mpld3
from bokeh.core.enums import Enumeration
from bokeh.embed import components
from bokeh.models import HoverTool
from django.shortcuts import render


# Create your views here.

def index(request):
    from scipy.interpolate import CubicSpline, lagrange
    import random
    import numpy as np
    import matplotlib.pyplot as plt

    plt.style.use('seaborn-poster')
    if request.POST:
        print('1')
        if "random" in request.POST:
            print('11')
            x =sorted(random.sample(range(0, 100), 5))
            print(x)
            y = random.sample(range(0, 100), 5)
        else:
            x = [int(val) for val in request.POST.getlist('x')]
            y = [int(val) for val in request.POST.getlist('y')]
        # use bc_type = 'natural' adds the constraints as we described above
        CS = CubicSpline(x, y, bc_type='natural')
        x_cs = np.arange(0, 100)
        y_cs = CS(x_cs)
        LI = lagrange(x, y)
        x_l = x_cs
        y_l = LI(x_l)

        # bokeh try
        from bokeh.plotting import figure, show

        # prepare some data

        # create a new plot with a title and axis labels
        p = figure(title="Интерполяция функций", x_axis_label="x", y_axis_label="y",
                   sizing_mode="stretch_both", toolbar_location="below")
        # p.legend.location = "bottom_left"
        # p.legend.background_fill_alpha = 0.5
        # add a line renderer with legend and line thickness
        line1 = p.line(x=x_cs, y=y_cs, name="Кубический сплайн", legend_label="Кубический сплайн", line_width=3)
        line2 = p.line(x_l, y_l, legend_label="Полином Лагранжа", line_width=3, name="Полином Лагранжа", color='red')
        dot = p.dot(x, y, legend_label="Исходная точка", name='Исходная точка', line_width=3, color='green', size=25)
        hover1 = HoverTool(tooltips=[
            ("name", "$name"),
            ("(x,y)", "(@x, @y)"),
        ], attachment='left', renderers=[line1], mode='vline')
        hover2 = HoverTool(tooltips=[
            ("name", "$name"),
            ("(x,y)", "(@x, @y)"),
        ], attachment='right', renderers=[line2], mode='vline')
        hover3 = HoverTool(tooltips=[
            ("name", "$name"),
            ("(x,y)", "(@x, @y)"),
        ], attachment='vertical', renderers=[dot])
        # hover.tooltips = [
        #     ("name", "$name"),
        #     ("(x,y)", "(@x, @y)"),
        # ]
        # hover.attachment='above'
        # hover.renderers=[line1]
        # hover.mode = 'vline'
        # hover.point_policy = 'snap_to_data'
        p.add_tools(hover1)
        p.add_tools(hover2)
        p.add_tools(hover3)
        # show the results

        script, div = components(p)

        # labels = [f'x: {a}<br>y: {b}' for a, b in zip(x, y)]

        return render(request, "index.html", {"xy": zip(x_cs, y_cs, y_l), 'script': script, 'div': div})
    else:
        return render(request, "index.html", {"empty": True})
