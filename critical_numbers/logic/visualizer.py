# Author: M. Schaub, 2018, GIScience Heidelberg 

import pygal
from pygal.style import DefaultStyle
import webbrowser
import os
from . import get_data


def visualize(data, website=True):
    """creates a bar chart diagram wich shows\
       mapped and validated in % of each project"""
    default_style = DefaultStyle
    default_style.background = 'transparent'
    if len(data) > 16:
        width = 1800
        chart_size = 100
    elif len(data) > 8:
        width = 1200
        chart_size = 75
    else:
        width = 800
        chart_size = 50
    bar_chart = pygal.Bar(x_label_rotation=20, style=default_style, range=(0, 100), width=width)  # Create a bar graph object
    bar_chart.title = 'Mapped and Validated in %'
    bar_chart.x_labels = [d['name'] for d in data]
    bar_chart.y_lables = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    bar_chart.add(f'percent Mapped', [d['percentMapped'] for d in data])
    bar_chart.add(f'percent Validated', [d['percentValidated'] for d in data])
    
    if website:
        chart = bar_chart.render_data_uri()
        table = bar_chart.render_table(style=True)
        return chart, chart_size, table
    else:
        bar_chart.render_to_file('bar_chart.svg')  # Save the svg to a file

        webbrowser._tryorder = ['firefox', 'chrome', 'safari', 'edge']
        webbrowser.open('file://' + os.path.realpath('bar_chart.svg'))

        return 'Bar chart created.'
