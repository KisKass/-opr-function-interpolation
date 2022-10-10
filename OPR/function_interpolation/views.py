import mpld3
from django.shortcuts import render

# Create your views here.


def index(request):
    from scipy.interpolate import CubicSpline
    import numpy as np
    import matplotlib.pyplot as plt

    plt.style.use('seaborn-poster')
    x = [0, 1, 2,6]
    y = [1, 3, 2,3]

    # use bc_type = 'natural' adds the constraints as we described above
    f = CubicSpline(x, y, bc_type='natural')
    x_new = np.linspace(0, 6, 100)
    y_new = f(x_new)

    from bokeh.plotting import figure, show

    # prepare some data

    # create a new plot with a title and axis labels
    p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y")

    # add a line renderer with legend and line thickness
    p.line(x_new, y_new, legend_label="Temp.", line_width=2)

    # show the results
    show(p)

    fig = plt.figure(figsize=(10, 8))
    plt.plot(x_new, y_new, 'b')
    plt.plot(x, y, 'ro')
    plt.title('Cubic Spline Interpolation')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    html_str = mpld3.fig_to_html(fig)
    Html_file = open("index.html", "w")
    Html_file.write(html_str)
    Html_file.close()
    return render(request, "index.html", {"html_str": html_str})
