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
    apiRequestTimestamp = 'apiRequestTimestamp'

    stats = { 
            'name': name, 
            'percentMapped': percentMappedMean,
            'percentValidated': percentValidatedMean,
            'apiRequestTimestamp': apiRequestTimestamp,
            }
    return stats
