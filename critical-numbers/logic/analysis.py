from logic import converter
from shapely.geometry import shape


def arithmetic_mean(data):
    '''returns arithmetic mean of given list of stats'''
    percentMappedMean = 0
    percentValidatedMean = 0
    for d in data:
            percentMappedMean = percentMappedMean + d['percentMapped']
            percentValidatedMean = percentValidatedMean + d['percentValidated']
    percentMappedMean = percentMappedMean * 100 / (100 * len(data))
    percentValidatedMean = percentValidatedMean * 100 / (100 * len(data))

    name = 'Arithmetic mean'

    stats = {
            'name': name,
            'percentMapped': percentMappedMean,
            'percentValidated': percentValidatedMean,
            'aoi': converter.convert_to_geojson(data)
            }
    return stats


def intersected(mapswipe_projects, hot_tm_projects):
    intersected_projects = {"type": "FeatureCollection", "features": []}
    for mapswipe_feature in mapswipe_projects['features']:
        print(str(mapswipe_feature['properties']['id']))
        if mapswipe_feature['geometry'] is None:
            continue
        geom1 = shape(mapswipe_feature['geometry'])
        for hot_tm_feature in hot_tm_projects['features']:
            geom2 = shape(hot_tm_feature['geometry'])
            if geom1.intersects(geom2):
                intersected_projects['features'].append(mapswipe_feature)
                intersected_projects['features'].append(hot_tm_feature)
    return intersected_projects


def get_centroid(featureCollection):
    centroids = []
    for feature in featureCollection['features']:
        centroid = {}
        projectId = feature['properties']['projectId']
        geom = shape(feature['geometry'])
        centroid['projectId'] = projectId
        centroid['aoi'] = [
                geom.centroid.xy[1][0],
                geom.centroid.xy[0][0]
                ]
        centroids.append(centroid)
    return centroids
