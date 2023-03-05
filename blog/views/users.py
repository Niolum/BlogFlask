from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required

from blog.models import User
from blog.utils import allowed_file
from blog.forms import ProfileForm
from blog import db


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
        file = request.files["photo"]
        if file and allowed_file(file.filename):
            User.delete_image(user)
            photo_name, photo_path = User.save_image(file=file, username=username, id=user.id)
            user.username = username
            user.photo_name = photo_name
            user.photo_path = photo_path
            db.session.add(user)
            db.session.commit()
            flash("Данные пользователя были изменены")
            return redirect(url_for('users.profile', username=username))

        user.username = username
        db.session.add(user)
        db.session.commit()
        flash("Имя пользователя было изменено")
        return redirect(url_for('users.profile', username=username))
    else:
        return render_template('users/profile.html', user=user, form=form)