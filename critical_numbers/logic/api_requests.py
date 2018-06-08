import requests
import json
import datetime
from urllib import parse


def get_aoi(projectId):
    url = f'https://tasks.hotosm.org/api/v1/project/{projectId}/aoi?as_file=true'
    aoi = requests.get(url)
    if aoi.status_code == 200:
        return aoi.json()


def get_organisations():
    '''returns a list of organisations'''
    organisations = requests.get(
            'https://tasks.hotosm.org/api/v1/tags/organisations'
            )
    if organisations.status_code == 200:
        organisations = organisations.json()
        organisations = organisations['tags']
        return organisations
    else:
        return None


def get_campaign_tags():
    '''returns a list of campaign tags'''
    campaign_tags = requests.get(
            'https://tasks.hotosm.org/api/v1/tags/campaigns'
            )
    if campaign_tags.status_code == 200:
        campaign_tags = campaign_tags.json()
        campaign_tags = campaign_tags['tags']
        return campaign_tags
    else:
        return None


def get_stats(projectIds=None, organisation=None, campaign_tag=None):
    '''fetches stats from type https://tasks.hotosm.org/api/\
            for a list of projectIds, a organisation or a campaign tag\
            returns a list of dict with stats of ech project'''
    if projectIds is not None:
        return get_projectId_stats(projectIds)

    elif organisation is not None:
        organisation = parse.quote(organisation)
        url = f'https://tasks.hotosm.org/api/v1/project/search?organisationTag={organisation}'
        return get_search_stats(url)

    elif campaign_tag is not None:
        campaign_tag = parse.quote(campaign_tag)
        url = f'https://tasks.hotosm.org/api/v1/project/search?campaignTag={campaign_tag}'
        return get_search_stats(url)
    else:
        url = 'https://tasks.hotosm.org/api/v1/project/search?mapperLevel=ALL'
        return get_search_stats(url)


def get_projectId_stats(projectIds):
    '''fetches Stats for each project from \
            https://tasks.hotosm.org/api'''
    projectIds = list(set(projectIds))
    data = []
    timestamp = datetime.datetime.utcnow()
    for projectId in projectIds:
        url = f'https://tasks.hotosm.org/api/v1/stats/project/{projectId}'
        stats = requests.get(url)
        if stats.status_code == 200:
            stats = stats.json()
            del stats['created']
            del stats['lastUpdated']
            del stats['mapperLevel']
            del stats['shortDescription']
            del stats['aoiCentroid']
            stats['apiRequestTimestampUTC'] = '{:%Y-%m-%d %H:%M}'.format(
                    timestamp
                    )
            stats['aoi'] = get_aoi(projectId)
            data.append(stats)
    return data


def get_search_stats(base_url):
    '''fetches stats using search for organisation or campaign tag from\
            https://tasks.hotosm.org/api'''
    headers = {'Accept-Language': 'en'}
    result = requests.get(base_url, headers=headers)
    if result.status_code == 200:
        result = result.json()
        timestamp = datetime.datetime.utcnow()
        collection_stats = []
        pages = result['pagination']['pages']
        for i in range(result['pagination']['pages']):
            print(f'{int(i*100/pages)}%')
            url = f'{base_url}&page={i+1}'
            request = requests.get(url, headers=headers)
            request.raise_for_status()
            request = request.json()
            for stats in request['results']:
                del stats['mapperLevel']
                del stats['shortDescription']
                del stats['status']
                del stats['activeMappers']
                del stats['priority']
                del stats['locale']
                stats['apiRequestTimestampUTC'] = '{:%Y-%m-%d %H:%M}'.format(
                        timestamp
                        )
                stats['aoi'] = get_aoi(stats['projectId'])
                collection_stats.append(stats)
        return collection_stats
    else:
        return []
