import mpld3
from bokeh.embed import components
from django.shortcuts import render


# Create your views here.

def index(request):
    from scipy.interpolate import CubicSpline
    import numpy as np
    import matplotlib.pyplot as plt

    plt.style.use('seaborn-poster')
    if request.POST:

        x = [int(val) for val in request.POST.getlist('x')]
        y = [int(val) for val in request.POST.getlist('y')]

    else:
        x = [0, 1, 2, 6]
        y = [1, 3, 2, 3]
    # use bc_type = 'natural' adds the constraints as we described above
    f = CubicSpline(x, y, bc_type='natural')
    x_new = np.linspace(0, 6, 100)
    y_new = f(x_new)
    # bokeh try
    from bokeh.plotting import figure, show

    # prepare some data

    # create a new plot with a title and axis labels
    p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y")

    # add a line renderer with legend and line thickness
    p.line(x_new, y_new, legend_label="Temp.", line_width=2)

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

    return render(request, "index.html", {"xy":zip(x_new,y_new),'script': script, 'div': div})
