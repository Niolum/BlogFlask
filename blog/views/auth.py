from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user

from blog.models import User
from blog.utils import allowed_file
from blog.forms import RegistrationForm, LoginForm
from blog import db


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            flash(f"Пользователь c именем '{username}' уже зарегистрирован", "error")
        else:
            user = User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            file = request.files["photo"]
            if file and allowed_file(file.filename):
                user = User.query.filter_by(username=username).first()
                photo_name, photo_path = User.save_image(file=file, username=username, id=user.id)
                user.photo_name = photo_name
                user.photo_path = photo_path
                db.session.add(user)
                db.session.commit()
            flash("Пользователь был успешно создан", "success") 
            return redirect(url_for("home"))
  
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Неверный логин", "error")
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, password):
            flash("Неверный пароль", "error")
            return redirect(url_for('auth.login'))
        
        login_user(user)
        return redirect('/')

    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))