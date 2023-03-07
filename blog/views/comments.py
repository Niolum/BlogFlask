from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from blog import db
from blog.models import Comment
from blog.forms import CommentForm


comments = Blueprint("comments", __name__, url_prefix="/comments")

@comments.route("/<int:post_id>", methods=["GET"])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template("posts/post_detail.html", comments=comments)

@comments.route("/create_comment/<int:post_id>", methods=["GET", "POST"])
@login_required
def create_comment(post_id):
    form = CommentForm(request.form)

    if request.method == "POST":
        message = request.form["message"]

        comment = Comment(message=message, post_id=post_id, owner_id=current_user.id) 
        db.session.add(comment)
        db.session.commit()
        flash("Комментарий был создан") 
        return redirect(url_for("posts.get_post", id=post_id))
    
    return render_template("posts/post_detail.html", form=form)

@comments.route("/delte_comment/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.owner_id != current_user.id:
        flash("Вы не можете удалить чужой комментарий")
    
    post_id = comment.post_id

    db.session.delete(comment)
    db.session.commit()
    flash("Комментарий был успешно удален", "success")
    return redirect(url_for("posts.get_post", id=post_id))
