import os
from PIL import Image
from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from blog import db
from blog.models import Post, Tag, User
from blog.forms import PostForm, CommentForm
from blog.utils import allowed_file
from blog.config import Config
from blog.cache import cache


posts = Blueprint('posts', __name__, url_prefix='/posts')


@posts.route("/", methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def all_posts():
    posts = Post.query.all()
    return render_template("posts/post_list.html", posts=posts)

@posts.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm(request.form)
    title_page = "Создание новой статьи"
    form.tags.choices = [(t.id, t.title) for t in Tag.query.all()]
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        tags = form.tags.data

        post = Post.query.filter_by(title=title).first()
        if post:
            flash(f"Статья c таким названием уже существует", "error")
        else:
            user_id = current_user.id
            post = Post(title=title, body=body, author_id=user_id)
            for tag in tags:
                post.tags.append(Tag.query.filter_by(id=tag).first())
                db.session.add(post)
                db.session.commit()
            file = request.files["photo"]
            if file and allowed_file(file.filename):
                post = Post.query.filter_by(title=title).first()
                image_name, image_path = Post.save_image(file=file, id=post.id)
                post.image_name = image_name
                post.image_path = image_path
                db.session.add(post)
                db.session.commit()
            flash("Статья была успешно создана", "success") 
            return redirect(url_for("home"))
  
    return render_template("posts/new_post.html", form=form, title_page=title_page)

@posts.route("/<int:id>", methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def get_post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    return render_template("posts/post_detail.html", post=post, form=form)

@posts.route("/update_post/<int:id>", methods=["GET", "POST"])
@login_required
def update_post(id):
    title_page = "Изменить статью"
    post = Post.query.get_or_404(id)
    if post.author_id != current_user.id:
        flash("Вы не можете изменять чужую статью")
    
    form = PostForm(request.form)

    name_image = None

    form.title.default = post.title
    form.body.default = post.body
    if post.image_path and post.image_name:
        path_to_image = f"{Config.UPLOAD_FOLDER}" + "/" + f"{post.image_path}"
        form.photo.data = Image.open(path_to_image)
        name_image = path_to_image.split("/")[-1]
    form.submit.label.text = "Изменить статью"
    form.process()
    form.tags.choices = [(t.id, t.title) for t in Tag.query.all()]

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        tags = request.form.getlist('tags')
        post.title = title
        post.body = body
        post.updated = datetime.utcnow()
        post.tags = []

        for tag in tags:
            post.tags.append(Tag.query.filter_by(id=tag).first())

        file = request.files["photo"]

        if file and name_image != file.filename and allowed_file(file.filename):
            Post.delete_image(post)
            image_name, image_path = Post.save_image(file=file, id=post.id)
            post.image_name = image_name
            post.image_path = image_path
        
        db.session.add(post)
        db.session.commit()

        flash("Статья была успешно изменена", "success") 
        return redirect(url_for("posts.get_post", id=post.id))
    
    return render_template("posts/new_post.html", form=form, title_page=title_page)

@posts.route("/<int:id>", methods=["POST"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author_id != current_user.id:
        flash("Вы не можете удалить чужую статью")

    if post.image_path and post.image_name:
        Post.delete_image(post)
        path_to_folder = f"{Config.UPLOAD_FOLDER}/posts/{post.id}"
        os.rmdir(path_to_folder)
    db.session.delete(post)
    db.session.commit()
    flash('Статья была успешно удалена', 'success')
    return redirect(url_for("home"))

@posts.route("/<username>", methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def get_posts_by_username(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author_id=user.id).all()
    return render_template("posts/post_list.html", posts=posts)

@posts.route("/tag/<title>", methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def get_posts_by_tag(title):
    posts = Post.query.join(Post.tags).filter(Tag.title==title).order_by(Post.created.desc()).all()
    return render_template("posts/post_list.html", posts=posts)