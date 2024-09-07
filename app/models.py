from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_required
from flask import current_app
from . import login_manager
from datetime import datetime

# Agent model
class Agent(UserMixin, db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(255))
    description = db.Column(db.String(255))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    image_url = db.Column(db.String(255))
    phone = db.Column(db.String(15))
    appointments = db.relationship('Appointment', backref='agent', lazy=True)


    # defining default role for new agents
    def __init__(self, **kwargs):
        super(Agent, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    # role verification
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.Administer)

    # password hashing
    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        return self.is_admin


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
        return f'{self.name}'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    agents = db.relationship('Agent', backref='role', lazy=True)


    @staticmethod
    def insert_roles():
        roles = {
            'Agent': (Permission.AddService, False),
            'Admin': (Permission.Administer, True)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    Administer = 0x80
    AddService = 0x01



# appointments model
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)