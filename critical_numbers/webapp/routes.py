from flask import request, render_template, redirect, url_for, flash
from webapp import app
from webapp.forms import ProjectIdForm, OrganisationForm, CampaignTagForm
from logic import api_requests, visualizer, analysis
from functools import wraps


prefix = ''


@app.route(prefix + '/', methods=['GET', 'POST'])
def index():
    organisations = api_requests.get_organisations_from_api()
    return view()


@app.route(prefix + '/<list:projectIds>', defaults={'mean': None}, methods=['GET', 'POST'])
@app.route(prefix + '/<list:projectIds>/<string:mean>', methods=['GET', 'POST'])
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

    if data is not None:
        if mean:
            data = [analysis.arithmetic_mean(data)]
        chart, chart_size, table = visualizer.visualize(data, website=True)
    else:
        chart = None
        chart_size = None
        table = None

    if projectIdForm.validate_on_submit():
        projectIds = projectIdForm.projectId.data
        projectIds = projectIds.replace(' ', '+')
        if projectIdForm.average.data:
            return redirect(f'{prefix}/{projectIds}/mean')
        else:
            return redirect(f'{prefix}/{projectIds}')

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
    else:
        return render_template('template.html',
                                projectIdForm=projectIdForm,
                                organisationForm=organisationForm,
                                campaignTagForm=campaignTagForm,
                                chart=chart,
                                chart_size=chart_size,
                                table=table)


if __name__ == "__main__":
    app.run()
