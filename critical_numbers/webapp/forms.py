from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired
from logic import api_requests

class ProjectIdForm(FlaskForm):
    projectId = StringField('Project Id', validators=[DataRequired()])
    average = BooleanField('Average')
    submit = SubmitField()


class OrganisationForm(FlaskForm):
    organisations = api_requests.get_organisations_from_api()
    organisations = sorted(organisations)
    organisationsTuples = []
    for organisation in organisations:
        organisationsTuples.append((organisation.replace(' ','_'), organisation))

    organisation = SelectField('Organisation', choices=organisationsTuples, validators=[DataRequired()])
    average = BooleanField('Average')
    submit = SubmitField()


class CampaignTagForm(FlaskForm):
    campaign_tags = api_requests.get_campaign_tags_from_api()
    campaign_tags= sorted(campaign_tags)
    campaign_tags_tuples = []
    for campaign_tag in campaign_tags:
        campaign_tags_tuples.append((campaign_tag.replace(' ','_'), campaign_tag))
    campaign_tag = SelectField('Campaign tag', choices=campaign_tags_tuples, validators=[DataRequired()])
    average = BooleanField('Average')
    submit = SubmitField()
