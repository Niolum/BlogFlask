from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, validators, FileField


class ProfileForm(FlaskForm):
    username = StringField("Имя пользователя: ", validators=[validators.DataRequired()])
    photo = FileField("Аватарка", validators=[FileAllowed(["jpeg", "jpg", "png"])])
    submit = SubmitField("Изменить данные")