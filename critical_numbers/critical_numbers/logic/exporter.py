# Author: M. Schaub, 2018, GIScience Heidelberg 

import get_data
import csv
import json
from geomet import wkt


def export(data, i):
    if i == 'geojson':
        export_to_geojson(data)
    elif i == 'wkt':
        export_to_wkt(data)
    elif i == 'csv':
        export_to_csv(data)
    else:
        pass


def export_to_wkt(data):
    for d in data:
        projectId = d['projectId']
        with open(f'aoi-{projectId}.geojson', 'r') as geojsonfile:
            aoi = json.loads(geojsonfile)
        with open(f'aoi-{projectId}.wkt', 'w') as wktfile:
            wkt.dumps(aoi, wktfile)


def export_to_geojson(data):
    for d in data:
        projectId = d['projectId']
        with open(f'stats-{projectId}.json', 'w') as jsonfile:
            json.dump(d, jsonfile)


def export_to_csv(data):
    with open('stats.csv', 'w', newline='') as csvfile:
        fieldnames = [
                'projectId',
                'name',
                'campaignTag',
                'percentMapped',
                'percentValidated',
                'created',
                'lastUpdated',
                'apiRequestTimestamp',
                'aoiCentroid',
                'mapperLevel',
                'organisationTag',
                'shortDescription',
                'status']
        writer = csv.DictWriter(csvfile,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                                fieldnames=fieldnames,
                                extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)
