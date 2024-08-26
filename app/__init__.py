from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    oauth.init_app(app)

    # import models
    from app.models import Location, Agent

    # import routes
    from app.agent.routes import agent_bp
    app.register_blueprint(agent_bp, url_prefix='/api')

    from app.main.routes import main
    app.register_blueprint(main)

    # import auth routes
    from app.auth.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app