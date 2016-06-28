from flask_wtf.form import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class URLForm(Form):
    url = StringField('url',
                      id='xyz',
                      validators=[DataRequired()])

