# Author: M. Schaub, 2018, GIScience Heidelberg 

import io
import csv
import json
from geomet import wkt


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


def convert_to_csv(data, stats):
    csvfile = io.StringIO()
    for d in data:
        aoi = d['aoi']
        d['aoi'] = wkt.dumps(aoi, decimals=4)
    fieldnames = [
            'projectId',
            'name',
            'campaignTag',
            'organisationTag',
            'percentMapped',
            'percentValidated',
            'apiRequestTimestamp',
            'aoi',
            'status']
    writer = csv.DictWriter(csvfile,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL,
                            fieldnames=fieldnames,
                            extrasaction='ignore')
    writer.writeheader()
    writer.writerows(data)
    return csvfile
