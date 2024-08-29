from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_required
from . import login_manager
# Agent model
class Agent(UserMixin, db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    password_hash = db.Column(db.String(255))

    # password hashing
    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    @login_manager.user_loader
    def load_user(user_id):
        return Agent.query.get(int(user_id))

    def __repr__(self):
        return f'<Agent {self.name}, {self.email}>'

# Location model
class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    agents = db.relationship('Agent', backref='location', lazy=True)

    def __repr__(self):
        return '<Location %r>' % self.name