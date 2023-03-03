from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, FileField
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя: ", validators=[validators.DataRequired()])
    password = PasswordField("Пароль: ", [
        validators.DataRequired(),
        validators.EqualTo("confirm", message="Пароли должны совпадать")
    ])
    confirm = PasswordField("Повторите пароль: ")
    photo = FileField("Аватарка", validators=[FileAllowed(["jpeg", "jpg", "png"])])
    submit = SubmitField("Создать пользователя")


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя: ", validators=[validators.DataRequired()])
    password = PasswordField("Пароль: ", validators=[validators.DataRequired()])
    submit = SubmitField("Войти")


class ProfileForm(FlaskForm):
    username = StringField("Имя пользователя: ", validators=[validators.DataRequired()])
    photo = FileField("Аватарка", validators=[FileAllowed(["jpeg", "jpg", "png"])])
    submit = SubmitField("Изменить имя")
