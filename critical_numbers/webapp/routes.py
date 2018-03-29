from flask import request, render_template, redirect, url_for
from webapp import app
from webapp.forms import ProjectIdForm
from logic import api_requests, visualizer

prefix = '/critical_numbers'


@app.route(prefix + '/', methods=['GET', 'POST'])
def index():
    projectIdForm = ProjectIdForm(request.form)
    organisations = api_requests.get_organisations_from_api()
    if request.method == 'POST':
        projectIds = request.form['projectId']
        projectIds = projectIds.replace(' ', '+')
        return redirect(f'{prefix}/{projectIds}')
    return render_template('template.html',\
            projectIdForm=projectIdForm, organisations=organisations)


@app.route(prefix + '/<list:projectIds>', methods=['GET', 'POST'])
def show_chart(projectIds):
    projectIdForm = ProjectIdForm()
    data = api_requests.add(projectIds)
    organisations = api_requests.get_organisations_from_api()
    if request.method == 'POST':
        projectIds = request.form['projectId']
        projectIds = projectIds.replace(' ', '+')
        return redirect(f'{prefix}/{projectIds}')
    return render_template('template.html',\
            projectIdForm=projectIdForm, organisations=organisations, chart=visualizer.visualize(data, website=True))
    
    
@app.route(prefix + '/organisation/<string:organisation>', methods=['GET', 'POST'])
def get_organisation_projectIds(organisation):
    projectIdForm = ProjectIdForm()
    data = api_requests.get_organisation_stats_from_api(organisation)
    organisations = api_requests.get_organisations_from_api()
    return render_template('template.html',\
            projectIdForm=projectIdForm, organisations=organisations, chart=visualizer.visualize(data, website=True))


if __name__ == "__main__":
    app.run()
