# Author: M. Schaub, 2018, GIScience Heidelberg 

import io
import csv
import json
from geomet import wkt


def convert(data, i):
    if i == 'geojson':
        convert_to_geojson(data)
    elif i == 'wkt':
        convert_to_wkt(data)
    elif i == 'csv':
        convert_to_csv(data)
    else:
        pass


def convert_to_wkt(data):
    for d in data:
        projectId = d['projectId']
        with open(f'aoi-{projectId}.geojson', 'r') as geojsonfile:
            aoi = json.loads(geojsonfile)
        with open(f'aoi-{projectId}.wkt', 'w') as wktfile:
            wkt.dumps(aoi, wktfile)


def convert_to_geojson(data):
    for d in data:
        projectId = d['projectId']
        with open(f'stats-{projectId}.json', 'w') as jsonfile:
            json.dump(d, jsonfile)


def convert_to_csv(data):
    csvfile = io.StringIO()
    for d in data:
        aoiCentroid = d['aoiCentroid']
        d['aoiCentroid'] = wkt.dumps(aoiCentroid, decimals=4)
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
    print(data)
    print(csvfile)
    return csvfile

