from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class ProjectIdForm(FlaskForm):
    projectId = StringField()
    submit = SubmitField()
