import requests
import json
import datetime


def add(projectIds):
    projectIds = list(set(projectIds))
    data = []
    for id in projectIds:
        data.append(get_stats_from_api(id))
    return data


def get_stats_from_api(projectId):
    """fetches Stats for one ProjectId from \
            https://tasks.hotosm.org/api-docs\
            and saves/appends as (list of) dictonaries to a pickle file"""

    url = f'https://tasks.hotosm.org/api/v1/stats/project/{projectId}'
    stats = requests.get(url)

    if stats.status_code == 200:
        stats = stats.json()
        timestamp = datetime.datetime.now()
        stats['apiRequestTimestamp'] = '{:%Y-%m-%d %H:%M}'.format(timestamp)
        return stats
    elif stats.status_code == 404:
        return 'No projects found'
    else:
        return None


def get_aoi_from_api(projectId):
    url = f'https://tasks.hotosm.org/api/v1/project/{projectId}/aoi?as_file=true'
    aoi = requests.get(url)
    if aoi.status_code == 200:
        aoi = aoi.json()
        dir_name = 'output'

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file_name = f'aoi-{projectId}.geojson'
        file_path = os.path.join(dir_name, file_name)

        with open(file_path, 'w') as geojsonfile:
            json.dump(aoi, geojsonfile)
    elif aoi.status_code == 404:
        return 'No projects found'
    else:
        return None


def get_organisations_from_api():
    '''returns a list of organisations'''
    organisations = requests.get('https://tasks.hotosm.org/api/v1/tags/organisations')
    if organisations.status_code == 200:
        organisations = organisations.json()
        organisations = organisations['tags']
        return organisations
    elif organisations.status_code == 404:
        return 'No organisations found'
    else:
        return None


def get_campaign_tags_from_api():
    '''returns a list of campaign tags'''
    campaign_tags = requests.get('https://tasks.hotosm.org/api/v1/tags/campaigns')
    if campaign_tags.status_code == 200:
        campaign_tags = campaign_tags.json()
        campaign_tags = campaign_tags['tags']
        return campaign_tags
    elif organisations.status_code == 404:
        return 'No campaign tags found'
    else:
        return None


def get_organisation_stats_from_api(organisation):
    '''returns a list of project Ids from given organisation'''
    organisation = organisation.replace('_', '%20')
    url = f'https://tasks.hotosm.org/api/v1/project/search?organisationTag={organisation}'
    headers = {'Accept-Language': 'en'}
    result = requests.get(url, headers=headers)
    organisation_stats = [] 
    if result.status_code == 200:
        result = result.json()
        for i in range(result['pagination']['pages']):
            url = f'https://tasks.hotosm.org/api/v1/project/search?organisationTag={organisation}&page={i+1}'
            result = requests.get(url, headers=headers)
            result = result.json()
            for d in result["results"]:
                organisation_stats.append(d)
        return organisation_stats
    elif result.status_code == 404:
        return 'No projects found'
    else:
        return None


def get_campaign_tags_stats_from_api(campaign_tag):
    '''returns a list of project Ids from given campaign tags'''
    campaign_tag = campaign_tag.replace('_', '%20')
    url = f'https://tasks.hotosm.org/api/v1/project/search?campaignTag={campaign_tag}'
    headers = {'Accept-Language': 'en'}
    result = requests.get(url, headers=headers)
    campaign_tag_stats = [] 
    if result.status_code == 200:
        result = result.json()
        for i in range(result['pagination']['pages']):
            url = f'https://tasks.hotosm.org/api/v1/project/search?campaignTag={campaign_tag}&page={i+1}'
            result = requests.get(url, headers=headers)
            result = result.json()
            for d in result["results"]:
                campaign_tag_stats.append(d)
        return campaign_tag_stats
    elif result.status_code == 404:
        return 'No projects found'
    else:
        return None
