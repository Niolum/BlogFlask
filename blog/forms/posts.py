from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, validators, TextAreaField, FileField, SelectMultipleField


class PostForm(FlaskForm):
    title = StringField("Название статьи: ", validators=[validators.DataRequired()])
    body = TextAreaField("Текст статьи", validators=[validators.DataRequired()])
    photo = FileField("Картинка для статьи", validators=[FileAllowed(["jpeg", "jpg", "png"])])
    tags = SelectMultipleField("Теги", coerce=int, validators=[validators.DataRequired()])
    submit = SubmitField("Создать статью")