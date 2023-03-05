from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class TagForm(FlaskForm):
    title = StringField("Название тега: ", validators=[validators.DataRequired()])
    submit = SubmitField("Создать тег")