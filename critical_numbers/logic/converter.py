# Author: M. Schaub, 2018, GIScience Heidelberg 
import io
import csv
from geomet import wkt


def convert_to_csv(data):
    '''Converts a list of dict to csv. Returns csv.'''
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
            'apiRequestTimestampUTC',
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
