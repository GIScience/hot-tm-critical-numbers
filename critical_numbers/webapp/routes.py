from flask import request, render_template, redirect, url_for, flash, jsonify, send_file
from webapp import app
from webapp.forms import ProjectIdForm, OrganisationForm, CampaignTagForm, DownloadDataForm, ViewChartForm
from logic import api_requests, visualizer, analysis, converter
import io


prefix = '/critical_numbers'


@app.route(prefix + '/', methods=['GET', 'POST'])
def index():
    return view()


@app.route(prefix + '/projectid/<list:projectIds>', defaults={'mean': None}, methods=['GET', 'POST'])
@app.route(prefix + '/projectid/<list:projectIds>/<string:mean>', methods=['GET', 'POST'])
def show_chart_of_projectIds(projectIds, mean):
    data = api_requests.get_stats(projectIds=projectIds)
    if mean == 'mean':
        mean = True
    return view(data, mean)


@app.route(prefix + '/organisation/<string:organisation>/', defaults={'mean': None}, methods=['GET', 'POST'])
@app.route(prefix + '/organisation/<string:organisation>/<string:mean>', methods=['GET', 'POST'])
def show_chart_of_organisation_projects(organisation, mean):
    data = api_requests.get_stats(organisation=organisation)
    if mean == 'mean':
        mean = True
    return view(data, mean)


@app.route(prefix + '/campaign_tag/<string:campaign_tag>/', defaults={'mean': None}, methods=['GET', 'POST'])
@app.route(prefix + '/campaign_tag/<string:campaign_tag>/<string:mean>', methods=['GET', 'POST'])
def show_chart_of_campaignTag_projects(campaign_tag, mean):
    data = api_requests.get_stats(campaign_tag=campaign_tag)
    if type(data) is str:
        error = data
        return view(error=error)
    if mean == 'mean':
        mean = True
    return view(data, mean)


@app.route(prefix + '/map.html')
def show_map():
    return flask.send_file(url_for('static', filename='map.html'))


def view(data=None, mean=False):
    '''form validation, redirecting and template rendering for all sites'''
    projectIdForm = ProjectIdForm()
    organisationForm = OrganisationForm()
    campaignTagForm = CampaignTagForm()
    downloadDataForm = DownloadDataForm()
    viewChartForm = ViewChartForm()


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
        if download_data_as == 'geojson':
            return jsonify(converter.convert_to_geojson(data))
        elif download_data_as == 'csv':
            # StringIO is output of csv.write
            # BytesIO is required by send_file()
            csvStringIO = converter.convert_to_csv(data)
            csvBytesIO = io.BytesIO()
            csvBytesIO.write(csvStringIO.getvalue().encode('utf-8'))
            csvBytesIO.seek(0)
            return send_file(csvBytesIO,
                     attachment_filename="stats.csv",
                     as_attachment=True)

    elif viewChartForm.validate_on_submit():
        return visualizer.visualize_to_file(data, to_svg = True)

    else:
        if data is not None:
            print(data)
            print(len(data))
            if mean and len(data) > 1:
                data = [analysis.arithmetic_mean(data)]
            chart, chart_size, table = visualizer.visualize_for_website(data, mean)
            return render_template('template.html',
                                    projectIdForm=projectIdForm,
                                    organisationForm=organisationForm,
                                    campaignTagForm=campaignTagForm,
                                    downloadDataForm=downloadDataForm,
                                    viewChartForm=viewChartForm,
                                    chart=chart,
                                    chart_size=chart_size,
                                    table=table)
        else:
            return render_template('template.html',
                                    projectIdForm=projectIdForm,
                                    organisationForm=organisationForm,
                                    campaignTagForm=campaignTagForm,
                                    downloadDataForm=downloadDataForm,
                                    viewChartForm=viewChartForm)


if __name__ == "__main__":
    app.run()
