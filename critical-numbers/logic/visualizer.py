#Author: M. Schaub, 2018, GIScience Heidelberg 

import folium
import pygal
from pygal.style import DefaultStyle


def visualize_for_website(data, mean=False):
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
    table = bar_chart.render_table(style=True)

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

    bar_chart = visualize(data, width , x_label_rotation)

    return bar_chart.render_response()


def visualize(data, width, x_label_rotation, mean=False):
    """creates a bar chart diagram wich shows\
       mapped and validated in % of each project"""
    default_style = DefaultStyle
    default_style.background = 'transparent'
    bar_chart = pygal.Bar(x_label_rotation=x_label_rotation,
            style=default_style,
            range=(0, 100), width=width)  # Create a bar graph object
    bar_chart.title = 'Mapped and Validated in %'
    if not mean:
        bar_chart.x_labels = [str(d['projectId']) for d in data]
    bar_chart.y_lables = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    bar_chart.add(f'percent Mapped', [d['percentMapped'] for d in data])
    bar_chart.add(f'percent Validated', [d['percentValidated'] for d in data])

    return bar_chart


def visualize_to_map(data, marker=False):
    m = folium.Map()
    featureCollection = {"type": "FeatureCollection", "features": []}
    if marker:
        aoiCoordinates = []
        for d in data:
            aoi = d['aoi']['coordinates']
            aoiCoordinates.append(aoi)
        folium.features.PolygonMarker(locations=aoiCoordinates).add_to(m)
    else:
        for d in data:
            aoi = d['aoi']
            feature= {"type": "Feature", "geometry": aoi}
            featureCollection["features"].append(feature)
        folium.GeoJson(featureCollection).add_to(m)
    return m.render()
    m.save('webapp/static/map.html')