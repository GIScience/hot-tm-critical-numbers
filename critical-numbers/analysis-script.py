import json
import os
import sys
import requests
from logic import api_requests, analysis, converter

url = 'http://mapswipe-backend.geog.uni-heidelberg.de:8080/geoserver/ms_layers/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=ms_layers:projects_extents&outputFormat=application%2Fjson'

result = requests.get(url)
mapswipe_projects = result.json()

dirname = 'output'
#filename = sys.argv[1]
#if not os.path.exists(dirname):
    #os.makedirs(dirname)

#with open(filename, 'r') as f:
    #mapswipe_projects = json.load(f)

hot_tm_projects = api_requests.get_stats()
hot_tm_projects = converter.convert_to_geojson(hot_tm_projects)

filepath = os.path.join(dirname, 'hot-tm-projects.geojson')
with open(filepath, 'w') as f:
    json.dump(hot_tm_projects, f)
    print('geojson of all hot-tm projects succsesfully written to output folder')

intersected_projects = analysis.intersected(mapswipe_projects, hot_tm_projects)

filepath = os.path.join(dirname, 'intersected-projects.geojson')
with open(filepath, 'w') as f:
    json.dump(intersected_projects, f)
    print('geojson of intersected projects succsesfully written to output folder')
