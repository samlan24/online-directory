from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # secret key
    app.config['SECRET_KEY'] = 'hello'
    # import models
    from app.models import Location, Agent

    # import routes
    from app.agent.routes import agent_bp
    app.register_blueprint(agent_bp, url_prefix='/api')

    # import main pages of the app
    from app.main.routes import main
    app.register_blueprint(main)

    # import auth routes
    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app