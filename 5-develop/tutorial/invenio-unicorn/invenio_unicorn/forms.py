from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators


class RecordForm(FlaskForm):

    title = StringField(
        'Title', [validators.DataRequired()]
    )
    description = TextAreaField(
        'Description', [validators.DataRequired()]
    )
