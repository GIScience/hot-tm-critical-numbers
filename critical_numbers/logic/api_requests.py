import requests
import json
import datetime


def get_stats(cond, value):
    '''Chooses the right request function for getting data from api'''
    func_dict = {
            'projectId': get_projectId_stats_from_api,
            'organisation': get_organisation_stats_from_api,
            'campaign_tag': get_campaign_tag_stats_from_api
            }
    return func_dict[cond](value)


def get_aoi_from_api(projectId):
    url = f'https://tasks.hotosm.org/api/v1/project/{projectId}/aoi?as_file=true'
    aoi = requests.get(url)
    if aoi.status_code == 200:
        return aoi.json()


def get_organisations_from_api():
    '''returns a list of organisations'''
    organisations = requests.get('https://tasks.hotosm.org/api/v1/tags/organisations')
    if organisations.status_code == 200:
        organisations = organisations.json()
        organisations = organisations['tags']
        return organisations
    else:
        return None


def get_campaign_tags_from_api():
    '''returns a list of campaign tags'''
    campaign_tags = requests.get('https://tasks.hotosm.org/api/v1/tags/campaigns')
    if campaign_tags.status_code == 200:
        campaign_tags = campaign_tags.json()
        campaign_tags = campaign_tags['tags']
        return campaign_tags
    else:
        return None


def get_projectId_stats_from_api(projectIds):
    '''fetches Stats for each project from \
            https://tasks.hotosm.org/api-docs'''
    projectIds = list(set(projectIds))
    data = []
    for projectId in projectIds:
        url = f'https://tasks.hotosm.org/api/v1/stats/project/{projectId}'
        stats = requests.get(url)
        timestamp = datetime.datetime.utcnow()
        if stats.status_code == 200:
            stats = stats.json()
            stats['apiRequestTimestampUTC'] = '{:%Y-%m-%d %H:%M}'.format(timestamp)
            del stats['aoiCentroid']
            stats['aoi'] = get_aoi_from_api(projectId)
            data.append(stats)
    return data


def get_organisation_stats_from_api(organisation):
    '''returns a list of project Ids from given organisation'''
    organisation = organisation.replace('_', '%20')
    url = f'https://tasks.hotosm.org/api/v1/project/search?organisationTag={organisation}'
    headers = {'Accept-Language': 'en'}
    result = requests.get(url, headers=headers)
    organisation_stats = [] 
    timestamp = datetime.datetime.utcnow()

    if result.status_code == 200:
        result = result.json()
        for i in range(result['pagination']['pages']):
            url = f'https://tasks.hotosm.org/api/v1/project/search?organisationTag={organisation}&page={i+1}'
            request = requests.get(url, headers=headers)
            request = request.json()
            results = request['results']
            features = request['mapResults']['features']

            for r, f in zip(results, features):
                r['apiRequestTimestampUTC'] = '{:%Y-%m-%d %H:%M}'.format(timestamp)
                r['aoi'] = f['geometry']
                organisation_stats.append(r)
        return organisation_stats
    else:
        return []


def get_campaign_tag_stats_from_api(campaign_tag):
    '''returns a list of project Ids from given campaign tag'''
    campaign_tag = campaign_tag.replace('_', '%20')
    url = f'https://tasks.hotosm.org/api/v1/project/search?campaignTag={campaign_tag}'
    headers = {'Accept-Language': 'en'}
    result = requests.get(url, headers=headers)
    campaign_tag_stats = [] 
    timestamp = datetime.datetime.utcnow()

    if result.status_code == 200:
        result = result.json()
        for i in range(result['pagination']['pages']):
            url = f'https://tasks.hotosm.org/api/v1/project/search?campaignTag={campaign_tag}&page={i+1}'
            request = requests.get(url, headers=headers)
            request = request.json()
            results = request['results']
            features = request['mapResults']['features']
            for r, f in zip(results, features):
                r['apiRequestTimestampUTC'] = '{:%Y-%m-%d %H:%M}'.format(timestamp)
                r['aoi'] = f['geometry']
                campaign_tag_stats.append(r)
        return campaign_tag_stats
    else:
        return []
