from app import db

# Agent model
class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    # method to return a dictionary of the agent
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'location': self.location.name
        }

    def __repr__(self):
        return '<Agent %r>' % self.name

# Location model
class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    agents = db.relationship('Agent', backref='location', lazy=True)

    # method to return a dictionary of the location
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'agents': [agent.name for agent in self.agents]
        }

    def __repr__(self):
        return '<Location %r>' % self.name