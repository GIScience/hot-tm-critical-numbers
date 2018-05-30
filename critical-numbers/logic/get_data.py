# Not in use for website
# Aor API connector se api_requests.py

import pickle
import json
import os.path


def write_data_to_disk(data, overwrite=False):
    data = dedupe(data)
    dir_name = 'output'
    file_name = 'data.pickle'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    file_path = os.path.join(dir_name, file_name)

    if os.path.isfile(file_path) and not overwrite:
        data = data + get_data_from_disk()
        with open(file_path, 'wb') as picklefile:
            pickle.dump(data, picklefile)
    else:
        with open(file_path, 'wb') as picklefile:
            pickle.dump(data, picklefile)
    return None


def get_data_from_disk():
    '''returns a list of dictonaries or None'''
    dir_name = 'output'
    file_name = 'data.pickle'
    file_path = os.path.join(dir_name, file_name)

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as picklefile:
            data = pickle.load(picklefile)
        return data
    else:
        return None


def delete_data_from_disk(projectId):
    '''deletes all data related to a projectId'''
    data = get_data_from_disk()
    for index, d in enumerate(data):
        if d['projectId'] == projectId:
            del data[index]
            write_data_to_disk(data, overwrite=True)
            return 'Deletion succsessful.'
    return 'No match found.'


def dedupe(projectIds, refresh=False):
    '''dedupes either given projectIds list or projectsIds on disk'''
    data = get_data_from_disk()
    if data == None:
        return projectIds
    elif refresh:
        for projectId in projectIds:
            for index, d in enumerate(data):
                if d['projectId'] == projectId:
                    del data[index]
        write_data_to_disk(data, overwrite=True)
        return projectIds
    else:
        for d in data:
            for index, projectId in enumerate(projectIds):
                if d['projectId'] == projectId:
                    del projectIds[index]
        return projectIds
