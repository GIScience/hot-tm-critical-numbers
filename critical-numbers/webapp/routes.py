from flask import (
        render_template,
        redirect,
        url_for,
        jsonify,
        send_file,
        )
from webapp import app
from webapp.forms import (
        ProjectIdForm,
        OrganisationForm,
        CampaignTagForm,
        DownloadDataForm,
        DownloadDataFormGeoJson,
        ViewChartForm,
        )
from logic import (
       api_requests,
       visualizer,
       analysis,
       converter,
       )
from string import Template
from urllib import parse


prefix = '/critical_numbers'


@app.route(
        prefix + '/',
        methods=['GET', 'POST']
        )
def index():
    return view()


@app.route(
        prefix + '/projectid/<list:projectIds>',
        defaults={'mean': None},
        methods=['GET', 'POST']
        )
@app.route(
        prefix + '/projectid/<list:projectIds>/<string:mean>',
        methods=['GET', 'POST']
        )
def show_chart_of_projectIds(projectIds, mean):
    data = api_requests.get_stats(projectIds=projectIds)
    if mean is not None:
        mean = True
    return view(data, mean)


@app.route(
        prefix + '/organisation/<string:organisation>',
        defaults={'mean': None},
        methods=['GET', 'POST']
        )
@app.route(
        prefix + '/organisation/<string:organisation>/<string:mean>',
        methods=['GET', 'POST']
        )
def show_chart_of_organisation_projects(organisation, mean):
    data = api_requests.get_stats(organisation=organisation)
    if mean is not None:
        mean = True
    return view(data, mean)


@app.route(
        prefix + '/campaign_tag/<string:campaign_tag>',
        defaults={'mean': None},
        methods=['GET', 'POST']
        )
@app.route(
        prefix + '/campaign_tag/<string:campaign_tag>/<string:mean>',
        methods=['GET', 'POST']
        )
def show_chart_of_campaignTag_projects(campaign_tag, mean):
    data = api_requests.get_stats(campaign_tag=campaign_tag)
    if mean is not None:
        mean = True
    return view(data, mean)


def view(data=None, mean=None):
    '''form validation, redirecting and template rendering for all sites'''
    projectIdForm = ProjectIdForm()
    organisationForm = OrganisationForm()
    campaignTagForm = CampaignTagForm()
    viewChartForm = ViewChartForm()

    if mean:
        data = [analysis.arithmetic_mean(data)]
        downloadDataForm = DownloadDataFormGeoJson()
    else:
        downloadDataForm = DownloadDataForm()

    if projectIdForm.validate_on_submit():
        projectIds = projectIdForm.projectId.data
        projectIds = projectIds.replace(' ', '+')
        if projectIdForm.average.data:
            url = Template('$prefix/projectid/$projectIds/$mean')
            url = url.substitute(prefix=prefix, projectIds=projectIds, mean='mean')
            return redirect(url)
        else:
            url = Template('$prefix/projectid/$projectIds')
            url = url.substitute(prefix=prefix, projectIds=projectIds,)
            return redirect(url)

    elif organisationForm.validate_on_submit():
        organisation = organisationForm.organisation.data
        organisation = parse.quote(organisation)
        if organisationForm.average.data:
            url = Template('$prefix/organisation/$organisation/$mean')
            url = url.substitute(prefix=prefix, organisation=organisation, mean='mean')
            return redirect(url)
        else:
            url = Template('$prefix/organisation/$organisation')
            url = url.substitute(prefix=prefix, organisation=organisation)
            return redirect(url)

    elif campaignTagForm.validate_on_submit():
        campaign_tag = campaignTagForm.campaign_tag.data
        campaign_tag = parse.quote(campaign_tag)
        if campaignTagForm.average.data:
            url = Template('$prefix/campaign_tag/$campaign_tag/$mean')
            url = url.substitute(prefix=prefix, campaign_tag=campaign_tag, mean='mean')
            return redirect(url)
        else:
            url = Template('$prefix/campaign_tag/$campaign_tag')
            url = url.substitute(prefix=prefix, campaign_tag=campaign_tag)
            return redirect(url)

    elif downloadDataForm.validate_on_submit():
        download_data_as = downloadDataForm.download_data.data
        if download_data_as == 'geojson':
            if mean:
                return jsonify(data[0])
            else:
                return jsonify(converter.convert_to_geojson(data))
        elif download_data_as == 'csv':
            csvBytesIO = converter.convert_to_csv(data)
            return send_file(
                    csvBytesIO,
                    attachment_filename="stats.csv",
                    as_attachment=True,
                    )

    elif viewChartForm.validate_on_submit():
        return visualizer.visualize_to_file(data, to_svg=True)

    else:
        if data is None:
            return render_template(
                    'template.html',
                    projectIdForm=projectIdForm,
                    organisationForm=organisationForm,
                    campaignTagForm=campaignTagForm,
                    downloadDataForm=downloadDataForm,
                    viewChartForm=viewChartForm
                    )
        else:
            chart, chart_size, table = visualizer.visualize_for_website(
                    data,
                    mean,
                    )
            leaflet_map = visualizer.visualize_to_map(data, mean)
            return render_template(
                    'template.html',
                    projectIdForm=projectIdForm,
                    organisationForm=organisationForm,
                    campaignTagForm=campaignTagForm,
                    downloadDataForm=downloadDataForm,
                    viewChartForm=viewChartForm,
                    chart=chart,
                    chart_size=chart_size,
                    table=table,
                    leaflet_map=leaflet_map
                    )


if __name__ == "__main__":
    app.run()
