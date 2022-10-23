import mpld3
from bokeh.embed import components
from bokeh.models import HoverTool
from django.shortcuts import render


# Create your views here.

def index(request):
    from scipy.interpolate import CubicSpline, lagrange

    import numpy as np
    import matplotlib.pyplot as plt

    plt.style.use('seaborn-poster')
    if request.POST:

        x = [int(val) for val in request.POST.getlist('x')]
        y = [int(val) for val in request.POST.getlist('y')]
        # use bc_type = 'natural' adds the constraints as we described above
        CS = CubicSpline(x, y, bc_type='natural')
        x_cs = np.linspace(min(x), max(x), 100)
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

        # add a line renderer with legend and line thickness
        p.line(x=x_cs, y=y_cs, name="Кубический сплайн", legend_label="Кубический сплайн", line_width=3)
        p.line(x_l, y_l, legend_label="Лагранж", line_width=3, color='red')
        p.dot(x, y, legend_label="Исходные точки", line_width=3, color='green', size=25)
        hover = HoverTool()
        hover.tooltips = [
            ("index", "$index"),
            ("name", "$name"),
            # ("(x_cs,y_cs,y_l)", "($x_cs, $y_cs, $y_l)"),
            ("(x,y)", "($x, $y)"),
            ("desc", "@desc"),
        ]
        # hover.anchor='left'
        hover.mode = 'vline'
        # hover.point_policy = 'snap_to_data'
        p.add_tools(hover)
        # show the results
        script, div = components(p)

        # fig, ax1 = plt.subplots(figsize=(10, 6))
        # ax1.plot(x_new, y_new, 'b')
        # ax1.plot(x, y, 'ro')
        # plt.title('Cubic Spline Interpolation')
        # plt.xlabel('x')
        # plt.ylabel('y')
        #
        # labels = [f'x: {a}<br>y: {b}' for a, b in zip(x, y)]
        #
        # position = mpld3.plugins.MousePosition()
        # mpld3.plugins.connect(fig, position)
        #
        # # tooltip = mpld3.plugins.PointLabelTooltip(fig, labels=labels)
        # tooltip = mpld3.plugins.PointHTMLTooltip(fig, labels=labels)
        # mpld3.plugins.connect(fig, tooltip)
        #
        # # print(labels)
        # # plt.show()
        # html_str = mpld3.fig_to_html(fig) "html_str": html_str,

        return render(request, "index.html", {"xy": zip(x_cs, y_cs, y_l), 'script': script, 'div': div})
    else:
        return render(request, "index.html", {"empty":True})
