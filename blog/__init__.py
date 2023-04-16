from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_moment import Moment
from whitenoise import WhiteNoise

from .config import ProductionConfig
from .cache import cache


db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()
moment = Moment()

def create_app():
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)

    db.init_app(app)
    
    cache.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    ckeditor.init_app(app)
    moment.init_app(app)

    with app.app_context():
        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        @app.route("/")
        def home():
            return redirect(url_for("posts.all_posts"))

        from blog.views import auth
        app.register_blueprint(auth)

        from blog.views import users
        app.register_blueprint(users)

        from blog.views import tags
        app.register_blueprint(tags)

        from blog.views import posts
        app.register_blueprint(posts)

        from blog.views import comments
        app.register_blueprint(comments)
    
    app.wsgi_app = WhiteNoise(
        app.wsgi_app, 
        root="blog/static"
    )

    return app