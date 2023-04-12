import os
from PIL import Image

from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user

from blog import db
from blog.models import User
from blog.utils import allowed_file
from blog.forms import ProfileForm
from blog.config import Config



users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=['GET'])
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
    form.username.default = user.username
    if user.photo_path and user.photo_name:
        path_to_image = f"{Config.UPLOAD_FOLDER}" + "/" + f"{user.photo_path}"
        form.photo.data = Image.open(path_to_image)
    form.process()
    if request.method == 'POST':
        username_new = request.form['username']
        if username != username_new:
            if User.query.filter_by(username=username_new).first():
                flash(f"Пользователь c именем '{username_new}' уже зарегистрирован", "error")
                return redirect(url_for('users.profile', username=username))
        file = request.files["photo"]
        if file and allowed_file(file.filename):
            User.delete_image(user)
            photo_name, photo_path = User.save_image(file=file, username=username, id=user.id)
            user.username = username_new
            user.photo_name = photo_name
            user.photo_path = photo_path
            db.session.add(user)
            db.session.commit()
            flash("Данные пользователя были изменены", "success")
            return redirect(url_for('users.profile', username=username_new))

        user.username = username_new
        db.session.add(user)
        db.session.commit()
        flash("Имя пользователя было изменено", "success")
        return redirect(url_for('users.profile', username=username_new))
    else:
        return render_template('users/profile.html', user=user, form=form)
    
@users.route("/myprofile/<username>/delete", methods=["POST"])
@login_required
def delete_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Данного юзера не существует", "error")

    if user.photo_path and user.photo_name:
        User.delete_image(user)
        path_to_folder = f"{Config.UPLOAD_FOLDER}/users/{user.id}/{user.username}"
        os.rmdir(path_to_folder)
        os.rmdir(path_to_folder.replace(f"/{username}", ""))
    db.session.delete(user)
    db.session.commit()
    flash("Профиль был успешно удален", "success")
    return redirect(url_for("home"))