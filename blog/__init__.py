from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template
from flask_login import LoginManager

from .config import Config


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
    
    migrate.init_app(app, db, compare_type=True)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def home():
        return render_template('index.html', title='Главная страница')

    from blog.views import auth
    app.register_blueprint(auth)

    from blog.views import users
    app.register_blueprint(users)

    from blog.views import tags
    app.register_blueprint(tags)
    
    return app