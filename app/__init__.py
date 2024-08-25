from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # import models
    from app.models import Location, Agent

    # import routes
    from app.agent.routes import agent_bp
    app.register_blueprint(agent_bp, url_prefix='/api')

    from app.main.routes import main
    app.register_blueprint(main)

    return app