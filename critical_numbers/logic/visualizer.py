# Author: M. Schaub, 2018, GIScience Heidelberg
from io import BytesIO
import folium
import pygal
from pygal.style import DefaultStyle
from . import converter, analysis


def visualize_for_website(data, mean):
    if len(data) > 16:
        width = 1800
        chart_size = 100
        x_label_rotation = 90
    elif len(data) > 8:
        width = 1200
        chart_size = 75
        x_label_rotation = 45
    else:
        width = 800
        chart_size = 50
        x_label_rotation = 0

    bar_chart = visualize(data, width, x_label_rotation, mean)

    chart = bar_chart.render_data_uri()
    #table = bar_chart.render_table(style=True)
    table=None

    return chart, chart_size, table


def visualize_to_file(data, to_svg):
    if len(data) > 16:
        width = 1800
        x_label_rotation = 90
    elif len(data) > 8:
        width = 1200
        x_label_rotation = 45
    else:
        width = 800
        x_label_rotation = 0

    bar_chart = visualize(data, width, x_label_rotation)

    chartBytesIO = BytesIO()
    chartBytesIO.write(bar_chart.render())
    chartBytesIO.seek(0)

    return chartBytesIO


def visualize(data, width, x_label_rotation, mean=None):
    """creates a bar chart diagram wich shows\
       mapped and validated in % of each project"""
    default_style = DefaultStyle
    default_style.background = 'transparent'
    bar_chart = pygal.Bar(
            x_label_rotation=x_label_rotation,
            style=default_style,
            range=(0, 100),
            width=width
            )
    bar_chart.title = 'Mapped and Validated in %'
    if mean is None:
        bar_chart.x_labels = [str(d['projectId']) for d in data]
    bar_chart.y_lables = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    bar_chart.add(f'percent Mapped', [d['percentMapped'] for d in data])
    bar_chart.add(f'percent Validated', [d['percentValidated'] for d in data])

    return bar_chart


def visualize_to_map(data, mean):
    m = folium.Map(tiles='Mapbox Bright', zoom_start=2)
    featureCollection = {"type": "FeatureCollection", "features": []}
    if mean:
        featureCollection = data[0]['aoi']
    else:
        featureCollection = converter.convert_to_geojson(data)
    folium.GeoJson(featureCollection).add_to(m)
    centroids = analysis.get_centroid(featureCollection)
    for centroid in centroids:
        folium.Marker(
                location=centroid['aoi'],
                popup=str(centroid['projectId'])
                ).add_to(m)
    m = m.get_root()
    m = m.render()
    return m
