# Author: M. Schaub, 2018, GIScience Heidelberg
import io
import csv
from geomet import wkt


def convert_to_csv(data):
    '''Converts a list of dict to csv. Returns csv.'''
    csvStringIO = io.StringIO()
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
            'apiRequestTimestampUTC',
            'aoi',
            'status']
    writer = csv.DictWriter(csvStringIO,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL,
                            fieldnames=fieldnames,
                            extrasaction='ignore')
    writer.writeheader()
    writer.writerows(data)

    # BytesIO is required by falsks send_file()
    csvBytesIO = io.BytesIO()
    csvBytesIO.write(csvStringIO.getvalue().encode('utf-8'))
    csvBytesIO.seek(0)

    return csvBytesIO


def convert_to_geojson(data):
    featureCollection = {"type": "FeatureCollection", "features": []}
    for stats in data:
        aoi = stats['aoi']
        del stats['aoi']
        if aoi is None:
            feature = {
                    "type": "Feature",
                    "geometry": None,
                    "properties": stats
                    }
        else:
            feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": aoi['type'],
                        "coordinates": aoi['coordinates']
                        },
                    "properties": stats
                    }
        featureCollection['features'].append(feature)
    return featureCollection
