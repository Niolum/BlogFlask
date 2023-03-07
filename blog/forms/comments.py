from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, TextAreaField


class CommentForm(FlaskForm):
    message = TextAreaField("Комментарий", validators=[validators.DataRequired()])
    submit = SubmitField("Отправить")