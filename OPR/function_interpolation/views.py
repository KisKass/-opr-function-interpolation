import io

import mpld3
import xlsxwriter
from bokeh.core.enums import Enumeration
from bokeh.embed import components
from bokeh.models import HoverTool
from django.http import HttpResponse
from django.shortcuts import render
from numpy import sin

# Create your views here.
global x_cs
global y_cs
global y_l


def excel(request):
    responce = generate_excel(x_cs, y_cs, y_l)
    return responce


def index(request):
    from scipy.interpolate import CubicSpline, lagrange
    import random
    import numpy as np
    import matplotlib.pyplot as plt

    plt.style.use('seaborn-poster')
    if request.POST:
        if "random" in request.POST:
            x = sorted(random.sample(range(0, 100), 5))
            print(x)
            y = random.sample(range(0, 100), 5)
        else:
            x = [float(val) for val in request.POST.getlist('x')]
            y = [float(val) for val in request.POST.getlist('y')]
        # use bc_type = 'natural' adds the constraints as we described above
        global x_cs
        global y_cs
        global y_l

        if max(x) < 100:
            x_lim = 100
        else:
            x_lim = max(x)
        print(x, max(x), x_lim)
        CS = CubicSpline(x, y, bc_type='natural')
        x_cs = np.arange(0, x_lim + 1)
        y_cs = CS(x_cs)
        LI = lagrange(x, y)
        x_l = x_cs
        y_l = LI(x_l)
        # xt = x_cs
        # yt = sin(xt*0.3)*100
        # for x in xt:
        #     print(x,yt[x])
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
        # line3 = p.line(xt, yt, legend_label='true function', line_width=3)
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


def generate_excel(x_cs, y_cs, y_l):
    import os

    # path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'hello.xlsx')
    try:
        os.remove('hello.xlsx')
    except:
        pass
    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()

    # Even though the final file will be in memory the module uses temp
    # files during assembly for efficiency. To avoid this on servers that
    # don't allow temp files, for example the Google APP Engine, set the
    # 'in_memory' Workbook() constructor option as shown in the docs.
    workbook = xlsxwriter.Workbook(output)

    worksheet = workbook.add_worksheet()

    merge_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
    })
    worksheet.merge_range('A1:С1', 'Результат интерполяции', merge_format)

    worksheet.write('A2', 'Х')
    worksheet.write('B2', 'Кубический сплайн')
    worksheet.write('С2', 'Полином Лагранжа')

    col = 0
    row = 2
    for r in x_cs:
        worksheet.write(row, col, r)
        row += 1

    col = 1
    row = 2
    for r in y_cs:
        worksheet.write(row, col, (r))
        row += 1

    col = 2
    row = 2
    for r in y_l:
        worksheet.write(row, col, (r))
        row += 1

    # Create a new chart object.
    chart = workbook.add_chart({'type': 'line'})

    # Configure the first series.
    chart.add_series({
        'name': 'Кубический сплайн',
        'categories': f'=Sheet1!$A$3:$A${row - 2}',
        'values': f'=Sheet1!$B$3:$B${row - 2}',
    })
    chart.add_series({
        'name': 'Полином Лагранжа',
        'categories': f'=Sheet1!$A$3:$A${row - 2}',
        'values': f'=Sheet1!$C$3:$C${row - 2}',
    })
    # Insert the chart into the worksheet.
    worksheet.insert_chart('D1', chart)

    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)

    # Set up the Http response.
    filename = 'otchet.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
