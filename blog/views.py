from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user

from .models import User
from .forms import RegistrationForm, LoginForm, ProfileForm
from . import db


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            flash(f"Пользователь c именем {username} уже зарегистрирован", 'danger')
        else:
            file = None
            if request.files['photo']:
                file = request.file["photo"]
        
            if file:
                photo_name, photo_url = User.save_image(image_data=file, username=username)
                user = User(username=username, password=generate_password_hash(password), photo_name=photo_name, photo_url=photo_url)
                db.session.add(user)
                db.session.commit()
                flash('Пользователь был успешно создан') 
                return redirect(url_for("home"))

            user = User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash('Пользователь был успешно создан') 
            return redirect(url_for("home"))
  
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not User or not check_password_hash(user.password, password):
            flash('Пожалуйста, проверьте данные для входа и повторите попытку', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect('/')

    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/users', methods=['GET'])
def all_users():
    users = User.query.all()
    return render_template('users/user_list.html', users=users)


@users.route('/<username>', methods=['GET'])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('users/user.html', user=user)


@users.route('/myprofile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    form = ProfileForm(request.form)
    user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        username = request.form['username']

        user.username = username
        db.session.add(user)
        db.session.commit()
        flash("Имя пользователя было изменено")
        return redirect(url_for('users.profile', username=username))
    else:
        return render_template('users/profile.html', user=user, form=form)