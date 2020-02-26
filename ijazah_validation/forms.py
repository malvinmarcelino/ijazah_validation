from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import re

class RecognitionForm(FlaskForm):
    ijazah = FileField('Ijazah', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])

    name = StringField('Name', validators=[
        DataRequired()
    ])

    institution = StringField('Institution', validators=[
        DataRequired()
    ])

    submit = SubmitField('Validate')