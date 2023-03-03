import datetime

from flask_login import UserMixin

from blog import db
from blog.config import BASE_DIR


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    photo_name = db.Column(db.String, nullable=True)
    photo_path = db.Column(db.String, nullable=True)
    posts = db.relationship('Post', lazy='select', backref=db.backref('user', lazy='joined'))
    comments = db.relationship('Comment', lazy='select', backref=db.backref('user', lazy='joined'))

    def __repr__(self):
        return f"User {self.username}"
    
    @staticmethod
    def save_image(image_data, username):
        with open(f"{BASE_DIR}/media/users/{username}/avatar.png", "w") as file:
            file.write(image_data)
        image_name = f"{username}_avatar"
        image_path = f"{BASE_DIR}/media/users/{username}/avatar.png"
        return image_name, image_path


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, index=True, unique=True)
    body = db.Column(db.String, nullable=False)
    image_name = db.Column(db.String, nullable=True)
    image_path = db.Column(db.String, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comments = db.relationship('Comment', lazy='select', backref=db.backref('post', lazy='joined'))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f"Post {self.title}"
    
    def save_image(self, image_data, id):
        with open(f"{BASE_DIR}/media/posts/{id}/post.png", "w") as file:
            file.write(image_data)
        image_name = f"{id}_post"
        image_path = f"{BASE_DIR}/media/posts/{id}/post.png"
        return image_name, image_path
    

class Tag(db.Model):
    __tablename__= 'tag'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True, index=True, unique=True)

    def __repr__(self):
        return f"Tag {self.title}"


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Comment {self.id} - {self.owner_id} - {self.post_id}"
