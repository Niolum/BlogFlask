from flask import Blueprint, render_template, request, flash, redirect, url_for

from blog import db
from blog.models import Tag
from blog.forms import TagForm


tags = Blueprint("tags", __name__, url_prefix="/tags")


@tags.route("/", methods=["GET"])
def all_tags():
    tags = Tag.query.all()
    return render_template("tags/tag_list.html", tags=tags)

@tags.route("/new_tag", methods=["GET", "POST"])
def new_tag():
    form = TagForm(request.form)
    if request.method == "POST":
        title = request.form["title"]

        tag = Tag.query.filter_by(title=title).first()
        if tag:
            flash(f"Тег c именем {title} уже существует", "danger")
        else:
            tag = Tag(title=title)
            db.session.add(tag)
            db.session.commit()
            flash("Тег был успешно создан") 
            return redirect(url_for("home"))
    
    return render_template("tags/new_tag.html", form=form)