from flask import Blueprint, request, jsonify
from app import db
from app.models import Agent, Location


agent_bp = Blueprint('agent', __name__)

# route to add an agent
@agent_bp.route('/agents', methods=['POST'])
def add_agent():
    data = request.get_json()

    # check if agent already exists if not add location
    location = Location.query.filter_by(name=data['location']).first()
    if location is None:
        location = Location(name=data['location'])
        db.session.add(location)
        db.session.commit()

    # create new agent
    new_agent = Agent(name=data['name'], email=data['email'], location_id=location.id)
    db.session.add(new_agent)
    db.session.commit()
    return jsonify({'message': 'New agent added!'})



# route to get all agents
@agent_bp.route('/agents', methods=['GET'])
def get_agents():
    agents = Agent.query.all()
    return jsonify([{'id': agent.id, 'name': agent.name, 'email': agent.email} for agent in agents])



# route to get an agent by id
@agent_bp.route('/agents/<int:agent_id>', methods=['GET'])
def get_agent(agent_id):
    agent = Agent.query.get(agent_id)
    if agent is None:
        return jsonify({'message': 'Agent not found!'}), 404
    else:
        return jsonify({'id': agent.id, 'name': agent.name, 'email': agent.email})


# route to update an agent
@agent_bp.route('/agents/<int:agent_id>', methods=['PUT'])
def update_agent(agent_id):
    agent = Agent.query.get(agent_id)
    if agent is None:
        return jsonify({'message': 'Agent not found!'}), 404
    else:
        data = request.get_json()
        location = Location.query.filter_by(name=data['location']).first()
        if location is None:
            return jsonify({'message': 'Location not found!'}), 404
        agent.name = data['name']
        agent.email = data['email']
        agent.location_id = location.id
        db.session.commit()
        return jsonify({'message': 'Agent updated!'})


# route to delete an agent
@agent_bp.route('/agents/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    agent = Agent.query.get(agent_id)
    if agent is None:
        return jsonify({'message': 'Agent not found!'}), 404
    else:
        db.session.delete(agent)
        db.session.commit()
        return jsonify({'message': 'Agent deleted!'})


# route to get all agents by location
@agent_bp.route('/agents/location/<string:location_name>', methods=['GET'])
def get_agents_by_location(location_name):
    location = Location.query.filter_by(name=location_name).first()
    if location is None:
        return jsonify({'message': 'Location not found!'}), 404
    agents = Agent.query.filter_by(location_id=location.id).all()
    return jsonify([{'id': agent.id, 'name': agent.name, 'email': agent.email, 'location': location.name} for agent in agents])

