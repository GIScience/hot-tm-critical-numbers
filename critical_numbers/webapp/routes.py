from flask import request, render_template, redirect, url_for, flash, jsonify
from webapp import app
from webapp.forms import ProjectIdForm, OrganisationForm, CampaignTagForm, DownloadDataForm
from logic import api_requests, visualizer, analysis
import json


prefix = '/critical_numbers'


@app.route(prefix + '/', methods=['GET', 'POST'])
def index():
    organisations = api_requests.get_organisations_from_api()
    return view()


@app.route(prefix + '/projectid/<list:projectIds>', defaults={'mean': None}, methods=['GET', 'POST'])
@app.route(prefix + '/projectid/<list:projectIds>/<string:mean>', methods=['GET', 'POST'])
def show_chart_of_projectIds(projectIds, mean):
    data = api_requests.add(projectIds)
    if mean == 'mean':
        mean = True
    return view(data, mean)


@app.route(prefix + '/organisation/<string:organisation>/', defaults={'mean': None}, methods=['GET', 'POST'])
@app.route(prefix + '/organisation/<string:organisation>/<string:mean>', methods=['GET', 'POST'])
def show_chart_of_organisation_projects(organisation, mean):
    data = api_requests.get_organisation_stats_from_api(organisation)
    if mean == 'mean':
        mean = True
    return view(data, mean)


@app.route(prefix + '/campaign_tag/<string:campaign_tag>/', defaults={'mean': None}, methods=['GET', 'POST'])
@app.route(prefix + '/campaign_tag/<string:campaign_tag>/<string:mean>', methods=['GET', 'POST'])
def show_chart_of_campaignTag_projects(campaign_tag, mean):
    data = api_requests.get_campaign_tags_stats_from_api(campaign_tag)
    if mean == 'mean':
        mean = True
    return view(data, mean)


def view(data=None, mean=False):
    '''form validation, redirecting and template rendering for all sites'''
    projectIdForm = ProjectIdForm()
    organisationForm = OrganisationForm()
    campaignTagForm = CampaignTagForm()
    downloadDataForm = DownloadDataForm()


    if projectIdForm.validate_on_submit():
        projectIds = projectIdForm.projectId.data
        projectIds = projectIds.replace(' ', '+')
        if projectIdForm.average.data:
            return redirect(f'{prefix}/projectid/{projectIds}/mean')
        else:
            return redirect(f'{prefix}/projectid/{projectIds}')

    elif organisationForm.validate_on_submit():
        organisation = organisationForm.organisation.data
        if organisationForm.average.data:
            return redirect(f'{prefix}/organisation/{organisation}/mean')
        else:
            return redirect(f'{prefix}/organisation/{organisation}/')

    elif campaignTagForm.validate_on_submit():
        campaign_tag = campaignTagForm.campaign_tag.data
        if campaignTagForm.average.data:
            return redirect(f'{prefix}/campaign_tag/{campaign_tag}/mean')
        else:
            return redirect(f'{prefix}/campaign_tag/{campaign_tag}/')

    elif downloadDataForm.validate_on_submit():
        download_data_as = downloadDataForm.download_data.data
        return jsonify(data)

    else:
        if data is not None:
            if mean:
                data = [analysis.arithmetic_mean(data)]
            chart, chart_size, table = visualizer.visualize(data, website=True)
            return render_template('template.html',
                                    projectIdForm=projectIdForm,
                                    organisationForm=organisationForm,
                                    campaignTagForm=campaignTagForm,
                                    downloadDataForm=downloadDataForm,
                                    chart=chart,
                                    chart_size=chart_size,
                                    table=table)
        else:
            return render_template('template.html',
                                    projectIdForm=projectIdForm,
                                    organisationForm=organisationForm,
                                    campaignTagForm=campaignTagForm,
                                    downloadDataForm=downloadDataForm)


if __name__ == "__main__":
    app.run()
